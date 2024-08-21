"""Dictionary helpers"""

# https://stackoverflow.com/questions/25833613/safe-method-to-get-value-of-nested-dictionary
def deep_get(_dict, keys, default=None):
    """Get nested-key value"""
    for key in keys:
        if isinstance(_dict, dict):
            _dict = _dict.get(key, default)
        else:
            return default
    return _dict