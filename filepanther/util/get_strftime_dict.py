import logging 
import sys

from filepanther.util.STRFTIME_MAP import STRFTIME_MAP


"""returns a dict with all strftime values as a dict"""
def get_strftime_dict(dt):
    logger = logging.getLogger("{}.{}".format(
        __name__,
        sys._getframe().f_code.co_name)
    )
    res = dict()
    for key in STRFTIME_MAP:
        if key in ["%%"]:  # skip these special directives
            continue
        split_key = STRFTIME_MAP[key].split(":")
        val = split_key[0].replace("{", "").replace("}", "")
        try:
            fmt_params = split_key[1].split("}")[0]
        except IndexError:  # no fmt params specified
            assert ":" not in STRFTIME_MAP[key]
            fmt_params = ""
        res[val] = dt.strftime(key)
    return res
