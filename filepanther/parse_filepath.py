"""
parse metadata out of a filepath
"""
import logging
import os

from parse import parse

from filepanther.get_filepath_formats import get_filepath_formats
from filepanther.util.replace_strftime_dirs import replace_strftime_dirs
from filepanther.util.strptime_parsed_pattern import strptime_parsed_pattern


def parse_filepath(
    metadb_handle,
    load_format=None,
    filepath=None,
    product_type_name=None,
    product_id=None,
    ingest_key=None,
    testing=False,
    **kwargs
):
    """
    Attempts to fill all arguments in args using args.filepath and information
    from `filepanther.data`. Tries to match against all possible product
    types if args.product_type_name is not given
    parse_filepath but for argparse namespaces

    params:
    -------
    metadb_handle: object with .get_records attr
        A handler for the metadata database that can be queried.

    returns:
    --------
    dict containing arguments parsed from filepath.
    """
    logger = logging.getLogger("filepanther.{}".format(
        __name__,
        )
    )
    logger.trace((
        "parse_filepath(\n\tfmt={},\n\tfpath={},\n\tpname={},\n\ting_k={},"
        "\n\tpid={}\n)"
        ).format(
            load_format, filepath, product_type_name, ingest_key, product_id
        )
    )
    args_dict = {}
    if (load_format is not None):
        args_parsed = _parse_from_product_type_and_filename(
            filepath,
            load_format,
            'manually set custom load_format',
            product_type_name,
            testing=testing
        )
    else:  # try all patterns (limiting by product name & ingest key if given)
        for pattern_name, pattern in get_filepath_formats(
            metadb_handle,
            short_name=product_type_name,
            ingest_name=ingest_key,
            product_id=product_id
        ).items():
            try:
                product_type_name = pattern_name.split(".")[0]
                args_parsed = _parse_from_product_type_and_filename(
                    filepath,
                    pattern,
                    pattern_name,
                    product_type_name,
                    testing=testing
                )
                break
            except SyntaxError as s_err:  # filepath does not match
                logger.trace("nope. caught error: \n>>>{}".format(s_err))
                product_type_name = None
        else:
            logger.warning("could not match filepath to any known patterns.")
            args_parsed = {}

    for key in args_parsed.keys():
        # TODO: args_dict = ...
        _set_unless_exists(args_dict, key, args_parsed[key])

    return args_dict


def _parse_from_product_type_and_filename(
    filepath, pattern, pattern_name, product_type_name,
    testing=False
):
    """
    Uses given pattern to parse args.filepath and fill any other arguments
    that can be inferred.

    args.product_type_name must be set before calling

    Returns:
    --------
    parsed_vars : dict
        dict of vars that were parsed from the given info
    """
    logger = logging.getLogger("filepanther.{}".format(
        __name__,
    ))
    logger.info("attempt parse as {}...".format(pattern_name))
    filename = filepath
    # switch to basepath if path info not part of pattern
    # logger.trace('fname: \n\t{}'.format(filename))
    # logger.trace('pattern: \n\t{}'.format(pattern))
    if "/" in filename:
        if "/" not in pattern:
            filename = os.path.basename(filename)
        elif pattern.startswith("/"):
            assert filename.startswith("/")  # must use absolute path
        else:
            # prepend variable to capture path
            pattern = "/{working_dir}/" + pattern

    # logger.debug('trying pattern "{}"'.format(pattern))
    logger.trace("\n{}\n\t=?=\n{}".format(filename, pattern))
    # logger.debug('args:\n{}'.format(args))

    path_fmt_str = replace_strftime_dirs(pattern)
    params_parsed = parse(path_fmt_str, filename)
    if params_parsed is None:
        raise SyntaxError(
            "filepath does not match pattern\n\tpath: {}\n\tpattern:{}".format(
                filename,
                path_fmt_str
            )
        )
        params_parsed = {}
    else:
        params_parsed = params_parsed.named

    dt = strptime_parsed_pattern(filename, pattern, params_parsed)

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

    parsed_vars['date_time'] = dt
    parsed_vars['time'] = dt.isoformat()
    logger.debug('date extracted: {}'.format(parsed_vars['time']))
    parsed_vars['product_type_name'] = product_type_name

    return parsed_vars


def _set_unless_exists(the_dict, key, val):
    """
    Sets the_dict[key] with val unless the_dict[key] already exists
    Like `the_dict.setdefault(key, val)`, but this *will* overwrite `None`.
    """
    if the_dict.get(key) is None:
        the_dict[key] = val
    return the_dict
