import json
import logging
import pickle
import sys 

from filepanther.filepath_to_metadata import filepath_to_metadata


def parse_filepath(
    filepath, 
    type_of_file=None, pattern=None, 
    pickle_fpath=None,
    verbose=False, quiet=False
):
    """get metadata from filepath"""
    logger = logging.getLogger("{}.{}".format(
        __name__,
        sys._getframe().f_code.co_name)
    )

    if type_of_file is None and pattern is None:
        logger.info("trying to guess file-pattern...")
        raise NotImplementedError(
            "filepath pattern guessing is not yet implemented"
        )
        # type_of_file = guess_filetype()
        # filepattern = get_filepattern(type_of_file)
    elif type_of_file is not None:
        raise NotImplementedError("filepath pattern types not yet implemented")
        # filepattern = get_filepattern(type_of_file)
    else:
        assert pattern is not None
    
    logger.info(f"parsing file using known file-pattern '{type_of_file}'")
    metadata = filepath_to_metadata(format_string=pattern, filepath=filepath)
    logger.trace(f"metadata:\n{metadata}")

    if pickle_fpath is not None:
        with open(pickle_fpath, "wb") as fhandle:
            pickle.dump(metadata, fhandle)
    del metadata["_datetime"]
    return json.dumps(metadata)
