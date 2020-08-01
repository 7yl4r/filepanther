from datetime import datetime
import logging
import os
from parse import parse

from filepanther.util.replace_strftime_dirs import replace_strftime_dirs
from filepanther.util.STRFTIME_MAP import STRFTIME_MAP


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

    # === parse named variables
    path_fmt_str = replace_strftime_dirs(format_string)
    params_parsed = parse(path_fmt_str, filepath)
    if params_parsed is None:
        raise SyntaxError(
            "filepath does not match pattern\n\tpath: {}\n\tpattern:{}".format(
                filepath,
                path_fmt_str
            )
        )
    # we only care about named param
    if len(params_parsed.fixed) > 0:
        raise ValueError(
            "All paramaters must be named ({thing1}), not fixed. ({})"
        )
    params_parsed = params_parsed.named

    # === parse datetime from pre-filled original format string
    if _contains_strptime_directives(format_string):
        prefilled_fmt_string = format_string.format(**params_parsed)
        params_parsed["_datetime"] = datetime.strptime(
            filepath, prefilled_fmt_string
        )

    logger.debug("params parsed from fname: \n\t{}".format(params_parsed))

    return params_parsed


def _contains_strptime_directives(fmt_str):
    for direc, fmt in STRFTIME_MAP.items():
        if direc in fmt_str:
            return True
    return False
