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
    # we only care about named params
    if len(params_parsed.fixed) > 0:
        raise ValueError(
            "All parameters must be named ({thing1}), not fixed. ({})"
        )
    params_parsed = params_parsed.named

    # === parse datetime from pre-filled original format string
    if _contains_strptime_directives(format_string):
        prefilled_fmt_string = format_string.format(**params_parsed)
        params_parsed["_datetime"] = _strptime_safe(
            filepath, prefilled_fmt_string
        )

    logger.debug("params parsed from fname: \n\t{}".format(params_parsed))

    return params_parsed


def _strptime_safe(input_str, fmt_str):
    """
    Wraps strptime to handle duplicate datetime directives.
    eg: "error: redefinition of group name..."
    """
    logger = logging.getLogger("filepanther.{}".format(
        __name__,
        )
    )
    # TODO: do we need to handle escapes:
    # fmt_str = fmt_str.replace("\%", "_P_")
    # fmt_str = fmt_str.replace("%%", "_PP_")
    directives = [str[0] for str in fmt_str.split('%')[1:]]
    new_str = fmt_str
    for dir, d_fmt in STRFTIME_MAP.items():
        d_varname = d_fmt[1:].split("}")[0].split(":")[0]
        dir = dir[1:]
        d_count = directives.count(dir)
        if d_count > 1:  # if duplicate
            logger.info(
                "Duplicate strptime directive detected."
                "Assuming all values equal; will throw ValueError if not."
            )
            read_value, new_str = _parse_multidirective(
                input_str, fmt_str, directive="%{}".format(dir)
            )
            fmt_str = fmt_str.replace(
                "%{}".format(dir),
                d_fmt.format(**{d_varname: read_value}),
                d_count - 1
            )
    return datetime.strptime(input_str, fmt_str)

# def _strptime_safe(fpath, prefilled_fmt_str):
#     """handles cases where there are duplicate strptime directives"""
#     for direc, fmt in STRFTIME_MAP.items():
#         # if multiple of a directive
#         if len(prefilled_fmt_str.split(direc)) > 2:
#             dt_vals = {}
#             # === split string and strptime each substring
#             for substr in prefilled_fmt_str.split(direc):
#                 dt_val_len = 1  # length of the date value (eg 4 for %Y)
#                 while dt_val_len > 24:  # longest directive possible is %c
#                     # keep adding chars until strptime works
#                     try:
#                         fpath_substr = fpath[:len(substr + dt_val_len)]
#                         dt_vals.append(datetime.strptime(
#                             fpath_substr, substr + direc
#                         ))
#                         # if datetime values do not match
#                         # !!! NOTE: this is going to happen a lot
#                         #       and I don't know how to deal with it.
#                         if len(dt_vals) > 1 and dt_vals[0] != dt_vals[-1]:
#                             dt_vals[0] == dt_vals[-2]
#                     except ValueError as err:  # strptime needs more chars
#                         assert "does not match format" in err.message
#                         dt_val_len += 1
#             if len(dt_vals) < 2:
#                 raise ValueError(
#                     "could not parse duplicate strftime directive"
#                 )


def _parse_multidirective(
    input_str, fmt_str, directive
):
    logger = logging.getLogger("filepanther.{}".format(
        __name__,
        )
    )
    logger.setLevel(5)
    n_duplicates = fmt_str.count(directive) - 1

    this_d_key = STRFTIME_MAP[directive].split(
        ":"
    )[0].replace('{', '').replace('}', '')

    this_d_fmt = STRFTIME_MAP[directive].split("}")[0].split(":")
    if len(this_d_fmt) == 2:
        this_d_fmt = this_d_fmt[1]
    else:
        this_d_fmt = ""

    logger.trace("parsing {}-duplicated dt '{}'...".format(
        n_duplicates, this_d_key
    ))
    dedirred_new_fmt_str = replace_strftime_dirs(fmt_str)
    logger.trace(
        "parse '{}' from strings:\n\t{}\n\t{}".format(
            directive,
            dedirred_new_fmt_str, input_str
        )
    )
    parsed_params = parse(dedirred_new_fmt_str, input_str)
    # assert that all parsed_params are equal
    if parsed_params is None:
        raise ValueError(
            "Failed to parse filepath with multiple strptime directives. "
            "Possible conflicting values found for same directive."
        )
    logger.trace(parsed_params)
    read_value = parsed_params[this_d_key]

    new_str = fmt_str.replace(  # fill all values except last one
        directive,
        ('{:' + this_d_fmt + '}').format(int(read_value)),
        n_duplicates
    )
    return read_value, new_str

def _contains_strptime_directives(fmt_str):
    for direc, fmt in STRFTIME_MAP.items():
        if direc in fmt_str:
            return True
    return False
