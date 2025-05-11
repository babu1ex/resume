import json


from typing import Callable


def process_json(
    json_str: str,
    required_keys: list[str] | None = None,
    tokens: list[str] | None = None,
    callback: Callable[[str, str], None] | None = None,
) -> None:
    json_str = json.loads(json_str)
    if required_keys is None:
        required_keys = []
    if tokens is None:
        tokens = []
    found_required_key = False
    for key in required_keys:
        if key in json_str:
            found_required_key = True
            break
    if not found_required_key:
        return
    for each_token in tokens:
        lower_token = each_token.lower()
        for each_required_key in required_keys:
            if each_required_key in json_str:
                if lower_token in json_str[each_required_key].lower():
                    if callback:
                        callback(each_required_key, each_token)
