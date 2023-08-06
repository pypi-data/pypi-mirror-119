"""
Mi.pyを使用する上でちょっとした際に便利なツール一覧
"""
import json
import re

import requests


def json_dump(data, *args, **kwargs):
    return json.dumps(data, ensure_ascii=False, *args, **kwargs)


def api(origin_uri: str, endpoint: str, data, files: dict = None) -> requests.models.Response:
    return requests.post(origin_uri + endpoint, data=data, files=files)


def upper_to_lower(data: dict, field: dict = None, nest=True) -> dict:
    if data is None:
        return {}
    replace_list: dict = {}
    pattern = re.compile('[A-Z]')
    if field is None:
        field = {}
    for attr in data:
        pattern = re.compile('[A-Z]')
        large = [i.group().lower() for i in pattern.finditer(attr)]
        result = [None] * (len(large + pattern.split(attr)))
        result[::2] = pattern.split(attr)
        result[1::2] = ['_' + i.lower() for i in large]
        default_key = "".join(result)
        if replace_list.get(attr):
            default_key = default_key.replace(attr, replace_list.get(attr))
        field[default_key] = data[attr]
        if type(field[default_key]) is dict and nest is True:
            field[default_key] = upper_to_lower(field[default_key])
    return field


def bool_to_string(boolean: bool) -> str:
    """
    boolを小文字にして文字列として返します

    Parameters
    ----------
    boolean : bool
        変更したいbool値
    Returns
    -------
    true or false: str
        小文字になったbool文字列
    """

    return 'true' if boolean else 'false'
