import logging
import sys 

def parse(filepath, type_of_file=None, verbose=False, quiet=False):
    """get metadata from filepath"""
    logger = logging.getLogger("{}.{}".format(
        __name__,
        sys._getframe().f_code.co_name)
    )

    if type_of_file is not None:
        logger.info("trying to guess file-pattern...")
        type_of_file = guess_filetype()
    logger.info(f"parsing file using known file-pattern '{type_of_file}'")
