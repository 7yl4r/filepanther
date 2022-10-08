import json
import logging
import pickle

from filepanther.metadata_to_filepath import metadata_to_filepath


def format_filepath(pickle_file, pattern, verbose=0, quiet=False):
    """fills a filepath pattern using data from json file"""
    with open(pickle_file, "rb") as pickle_fp:
        metadata = pickle.load(pickle_fp)
        return metadata_to_filepath(pattern, metadata)
