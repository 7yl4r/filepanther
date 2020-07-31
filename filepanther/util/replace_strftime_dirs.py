from filepanther.util.STRFTIME_MAP import STRFTIME_MAP


def replace_strftime_dirs(in_string):
    """Replaces strftime directives with something usable by parse()"""
    for direc, fmt in STRFTIME_MAP.items():
        in_string = in_string.replace(direc, fmt)
    return in_string
