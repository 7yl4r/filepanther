# File Panther
File paths are just poorly-structured metadata.
File Panther helps your programs parse and format metadata into filepaths.

## Requirements
* `python>=3.5.0`
    * for `*splat` usage

## setup
0. `git clone https://github.com/7yl4r/filepanther`
0. `cd filepanther`
1. `pip install -e .`
2. `pip install -r tests_requirements.txt`
3. `python -m pytest -m "not real_db"`

## usage examples
```python
metadata_dict = filepath_to_metadata(filepath, filepath_format_str)

filepath = metadata_to_filepath(metadata_dict, filepath_format_str)
```
