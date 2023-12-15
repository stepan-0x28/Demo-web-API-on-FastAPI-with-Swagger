from typing import Any, Dict


def remove_keys(dictionary: Dict[str, Any], *keys: str) -> Dict[str, Any]:
    for key in keys:
        if key in dictionary:
            del dictionary[key]

    return dictionary
