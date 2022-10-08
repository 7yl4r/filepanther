import json
import logging

from filepanther.metadata_to_filepath import metadata_to_filepath


def format_filepath(json_file, pattern, verbose=0, quiet=False):
    """fills a filepath pattern using data from json file"""
    with open(json_file) as json_fp:
        metadata = json.load(json_fp)
        return metadata_to_filepath(pattern, metadata)
