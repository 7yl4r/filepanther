from datetime import datetime
import logging

from parse import parse

from filepanther.parse_to_fmt_sanitize import parse_to_fmt_sanitize
from filepanther.util.replace_strftime_dirs import replace_strftime_dirs
from filepanther.util.STRFTIME_MAP import STRFTIME_MAP


def strptime_parsed_pattern(input_str, format_str, params):
    """
    Extracts datetime from given input_str matching given format_str.
    Parameters
    ----------
    params : dict
        named parameters from previous parse of input_str using format_str
    format_str : str
        original format string like "{whatever}-%Y.txt"
    input_str : str
        same raw input string as passed to parse()
    """
    format_str = parse_to_fmt_sanitize(format_str)
    # fill fmt string with all parameters (except strptime dirs)
    filled_fmt_str = format_str.format(**params)
    return _strptime_safe(input_str, filled_fmt_str)


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
