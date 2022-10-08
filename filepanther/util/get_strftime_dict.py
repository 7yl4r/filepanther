from filepanther.util.STRFTIME_MAP import STRFTIME_MAP

"""returns a dict with all strftime values as a dict"""
def get_strftime_dict(dt):
    res = dict()
    for key in STRFTIME_MAP:
        if key in ["%%"]:  # skip these special directives
            continue
        val = STRFTIME_MAP[key].split(":")[0].replace("{", "").replace("}", "")
        res[val] = dt.strftime(key)
    return res
