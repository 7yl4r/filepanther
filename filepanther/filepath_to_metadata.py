import logging

from parse import parse

from filepanther.util.replace_strftime_dirs import replace_strftime_dirs


def filepath_to_metadata(format_string, filepath):
    """
    Parses metadata from given filepath using the given format string.
    """
    # TODO: complete this & metadata_to_filepath and then create new branch
    #       with only these two fns.
    logger = logging.getLogger("filepanther.{}".format(
        __name__,
        )
    )
    filename = filepath
    path_fmt_str = replace_strftime_dirs(format_string)
    params_parsed = parse(path_fmt_str, filename)
    if params_parsed is None:
        raise SyntaxError(
            "filepath does not match pattern\n\tpath: {}\n\tpattern:{}".format(
                filename,
                path_fmt_str
            )
        )

    logger.debug("params parsed from fname: \n\t{}".format(params_parsed))
    # NOTE: setattr LAST here, else args will get set before we know
    #   that this filename matches the given pattern
    parsed_vars = {}
    for param in params_parsed:
        if param[:3] != "dt_":  # ignore these
            val = params_parsed[param]
            # arg_dict = _set_unless_exists(arg_dict, param, val)
            parsed_vars[param] = val
            # logger.debug('{} extracted :"{}"'.format(param, val))

    return parsed_vars
