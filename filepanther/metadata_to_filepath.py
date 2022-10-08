from filepanther.util.STRFTIME_MAP import STRFTIME_MAP


def metadata_to_filepath(format_string, metadata_dict):
    """
    Fills a given format string with given metadata.
    """

    # === insert vars from given dict:
    result = format_string.format(**metadata_dict)

    # === handle `dt_*` vars in metadata_dict and strftime directives in str
    for dir_key in metadata_dict:
        if dir_key.startswith("dt_"):
            # get the strftime directive key name (eg %Y for dt_Y)
            directive = dir_key.split("dt_")[1]
            directive = "%" + directive
            if directive in result:  # insert value
                # use value directly if string
                if isinstance(metadata_dict[dir_key], str):
                    result = result.replace(directive, metadata_dict[dir_key])
                else:  # format it to string accordingly
                    result = result.replace(directive, STRFTIME_MAP[directive])
                    result = result.format(**metadata_dict)
            # else diretive not in string, it's unused metadata
            # TODO: show warning about unused metadata?
    return result
