import atexit
import os
import urllib
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

import h5py
import pandas as pd
import logging as logg
import pytorch_lightning as pl
import torch
from Bio import SeqIO
from sklearn.model_selection import train_test_split
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm

from . import __version__
from .language_model import embed_from_fasta, lm_embed
from .utils import get_local_or_download


def collate_pairs_fn(args):
    """
    Collate function for PyTorch data loader.
    """
    x0 = pad_sequence([a[0] for a in args], batch_first=True)
    x1 = pad_sequence([a[1] for a in args], batch_first=True)
    y = [a[2] for a in args]
    return x0, x1, torch.stack(y, 0)


class CachedH5:
    def __init__(
        self, filePath: str, preload: bool = False, verbose: bool = False
    ):
        self.filePath = filePath
        self.seqMap = h5py.File(self.filePath, "r")
        self.seqs = self.seqMap.keys()
        self.preload = preload
        self.verbose = verbose
        if self.preload:
            self._embDict = {}
            for n in tqdm(self.seqs):
                self._embDict[n] = torch.from_numpy(self.seqMap[n][:])
        atexit.register(self.cleanup)

    def cleanup(self):
        self.seqMap.close()

    @lru_cache(maxsize=5000)
    def __getitem__(self, x):
        if self.preload:
            return self._embDict[x]
        else:
            return torch.from_numpy(self.seqMap[x][:])


class CachedFasta:
    def __init__(
        self, filePath: str, preload: bool = False, verbose: bool = False
    ):
        self.filePath = filePath
        self.seqMap = {
            r.name: str(r.seq) for r in SeqIO.parse(self.filePath, "fasta")
        }
        self.seqs = list(self.seqMap.keys())
        self.preload = preload
        self.verbose = verbose
        if self.preload:
            self._embDict = {}
            for (n, s) in tqdm(self.seqMap.items()):
                self._embDict[n] = lm_embed(s, verbose=self.verbose)

    @lru_cache(maxsize=5000)
    def __getitem__(self, x):
        if self.preload:
            return self._embDict[x]
        else:
            return lm_embed(self.seqMap[x], verbose=self.verbose)


class PairedEmbeddingDataset(Dataset):
    """
    Dataset to be used by the PyTorch data loader for pairs of sequences and their labels.

    :param x0: List of first name in the pair
    :param x1: List of second name in the pair
    :param y: List of labels
    :param embedding: Embeddings
    """

    def __init__(self, pair_df: pd.DataFrame, embedding: CachedH5):
        self.x0 = pair_df[0]
        self.x1 = pair_df[1]
        self.y = pair_df[2]
        self.embedding = embedding

    def __len__(self):
        return len(self.x0)

    def __getitem__(self, i):
        return (
            self.embedding[self.x0.iloc[i]],
            self.embedding[self.x1.iloc[i]],
            torch.tensor(self.y.iloc[i]),
        )


class PPIDataModule(pl.LightningDataModule):
    def __init__(
        self,
        sequence_path: str,
        pair_path: str,
        data_dir: str = os.getcwd(),
        batch_size: int = 64,
        shuffle: bool = True,
        augment_train: bool = True,
        train_val_split: List[float] = [0.9, 0.1],
    ):
        super().__init__()

        self.data_dir = Path(data_dir)
        self.sequence_path = Path(sequence_path)
        self.pair_path = Path(pair_path)
        self.augment_train = augment_train

        # If sequence_path is a URL, prepare for download
        url_seq = urllib.parse.urlparse(sequence_path)
        if url_seq.scheme in ["http", "https"]:
            self.sequence_path = self.data_dir / Path(
                os.path.basename(url_seq.path)
            )
            self.sequence_url = sequence_path
        else:
            self.sequence_url = None

        # If pair_path is a URL, prepare for download
        url_pair = urllib.parse.urlparse(pair_path)
        if url_pair.scheme in ["http", "https"]:
            self.pair_path = self.data_dir / Path(
                os.path.basename(url_pair.path)
            )
            self.pair_url = pair_path
        else:
            self.pair_url = None

        # Hyperparams
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.train_val_split = train_val_split

    def prepare_data(self):
        """
        Prepare data for DataModule.
        """
        get_local_or_download(self.sequence_path, self.sequence_url)

        # If sequence_path is not embeddings, embed
        if not self.sequence_path.suffix == ".h5":
            assert not self.sequence_path.with_suffix(".h5").exists()
            embed_from_fasta(
                self.sequence_path,
                self.sequence_path.with_suffix(".h5"),
                verbose=True,
            )
            self.sequence_path = self.sequence_path.with_suffix(".h5")

    def setup(self, stage: Optional[str] = None):

        self.embeddings = CachedH5(self.sequence_path)

        self.full_df = pd.read_csv(self.pair_path, sep="\t", header=None)
        self.full_df = self.full_df.sort_values([0, 1])

        self.train_df, self.val_df = train_test_split(
            self.full_df,
            train_size=self.train_val_split[0],
            test_size=self.train_val_split[1],
        )

        if self.augment_train:
            train_n0 = pd.concat((self.train_df[0], self.train_df[1]), axis=0)
            train_n1 = pd.concat((self.train_df[1], self.train_df[0]), axis=0)
            train_y = pd.concat((self.train_df[2], self.train_df[2]), axis=0)
            self.train_df = pd.concat([train_n0, train_n1, train_y], axis=1)

        self.data_train = PairedEmbeddingDataset(
            self.train_df, self.embeddings
        )

        self.data_val = PairedEmbeddingDataset(self.val_df, self.embeddings)

    def train_dataloader(self):
        return DataLoader(
            self.data_train,
            batch_size=self.batch_size,
            shuffle=self.shuffle,
            collate_fn=collate_pairs_fn,
        )

    def val_dataloader(self):
        return DataLoader(
            self.data_val,
            batch_size=self.batch_size,
            shuffle=self.shuffle,
            collate_fn=collate_pairs_fn,
        )

    def test_dataloader(self):
        return DataLoader(
            self.data_val,
            batch_size=self.batch_size,
            shuffle=self.shuffle,
            collate_fn=collate_pairs_fn,
        )

    def teardown(self):
        self.embeddings.cleanup()
