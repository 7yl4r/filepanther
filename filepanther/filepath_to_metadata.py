import logging
import os
from parse import parse

from filepanther.util.replace_strftime_dirs import replace_strftime_dirs


def filepath_to_metadata(format_string, filepath, basename_only=False):
    """
    Parses metadata from given filepath using the given format string.
    """
    # TODO: complete this & metadata_to_filepath and then create new branch
    #       with only these two fns.
    logger = logging.getLogger("filepanther.{}".format(
        __name__,
        )
    )
    if basename_only:
        format_string = os.path.basename(format_string)
        filepath = os.path.basename(filepath)
        logger.debug("parsing only on basenames")

    path_fmt_str = replace_strftime_dirs(format_string)
    params_parsed = parse(path_fmt_str, filepath)
    if params_parsed is None:
        raise SyntaxError(
            "filepath does not match pattern\n\tpath: {}\n\tpattern:{}".format(
                filepath,
                path_fmt_str
            )
        )

    logger.debug("params parsed from fname: \n\t{}".format(params_parsed))

    if len(params_parsed.fixed) > 0:
        raise ValueError(
            "All paramaters must be named ({thing1}), not fixed. ({})"
        )

    return params_parsed.named
