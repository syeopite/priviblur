from typing import List, Tuple


def dig_dict(target, keys: List | Tuple):
    """Digs through a dictionary. Returns none if a given key is missing"""
    for key in keys:
        if isinstance(target, dict):
            target = target.get(key)
        else:
            return None

    return target
