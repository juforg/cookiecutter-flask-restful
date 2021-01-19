from typing import List, Dict, Tuple

from {{cookiecutter.app_name}}.commons.exception import BizException


def group_by_for_list(data_list: List[Dict], by: List[str] = None,key_error: bool = False) -> Dict[Tuple, List]:
    """
    json数据group by
    :param key_error:
    :param data_list:   数据列表
    :param by:  group by 列表
    :return:   分组后的数据
    """
    if data_list is None or by is None:
        return data_list

    grouped_by_data = {}
    for data in data_list:
        key = []
        for b in by:
            if not b in data.keys() and key_error:
                raise BizException("key:[{}]不存在".format(b))
            key.append(data.get(b))

        key_tuple = tuple(key)
        values = grouped_by_data.get(key_tuple)
        if values is None:
            values = []
            grouped_by_data[key_tuple] = values
        values.append(data)

    return grouped_by_data
