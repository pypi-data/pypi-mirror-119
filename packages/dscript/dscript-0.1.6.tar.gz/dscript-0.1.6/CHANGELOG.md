# To Do
- Full logging system (issue #5)
- Add multi-gpu support (issue #6)
- Use multiple workers to load embeddings / support for loading embeddings on the fly to reduce memory usage (issue #8/11)
- Add convenience function to generate candidates - all pairs from a list / cartesian produt of multiple lists
- Add error handling for calledProcessError in utils.gpu_mem

# v0

## v0.1

### v0.1.6: 2021-09-06 -- Bug Fix - Augmentation and proper defaults
- Augmentation fix in v0.1.5 was bugged still and would throw an error, now resets index
- Change `--use-w` and `--augment` to `--no-w` and `--no-augment` with store false

### v0.1.5: 2021-06-23 -- Bug Fix - Augment and Documentation
- Updated package level imports 
- Updated documentation
- Fixed issue #13: improper augmentation of data
- Fixed issue #12: overwrites cmap data sets if they already exist

### v0.1.4: 2021-03-05 -- Bug Fix - Typo in `ContactModule.forward()`
- Fixed issue #7: bug which would crash contact module if called directly

### v0.1.3: 2021-02-17 -- Bug Fix - Pairs too large for GPU
- Fixed issues #3, #4
- Basic logging system implemented to report skipped pairs
- Fixed wrong variable name in loading from sequence file
- Updated documentation

### v0.1.2: 2020-11-30 -- Bug Fix - Eval Mode
- Model should be put into `eval()` mode before prediction or evaluation, and when new models are downloaded - this makes the output deterministic by disabling dropout layers

### v0.1.1: 2020-11-18 -- First Beta Release
