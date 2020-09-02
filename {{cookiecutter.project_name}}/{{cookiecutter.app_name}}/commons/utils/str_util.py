# -*- coding: utf-8 -*-

#  Copyright (c) ©2019, Cardinal Operations and/or its affiliates. All rights reserved.
#  CARDINAL OPERATIONS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

# @author: songjie@shanshu.ai
# @date: 2019/10/28
import re


def is_number(str_number: str):
    """
    判断字符串是否是数字(数字、小数、负数、负小数、0)
    :param str_number:
    :return:
    """

    if (str_number.split(".")[0]).isdigit() or str_number.isdigit() or (str_number.split('-')[-1]).split(".")[
        -1].isdigit():
        return True
    else:
        return False

def is_int(str_number: str):
    """
    判断字符串是否是整数 如果是正数 判断是否为数字 如果是负数 判断除掉负号的部分是否是数字
    :param str_number:
    :return:
    """
    return str_number.lstrip('-').isdigit()

def is_float(str_number: str):
    """
    判断字符串是否浮点
    :param str_number:
    :return:
    """
    value = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')  # 定义正则表达式
    return value.match(str_number)


def to_camel_case(text):
    arr = filter(None, text.lower().split('_'))
    # _snake_case = re.compile(r"(?<=\w)_(\w)")
    res = ''
    j = 0
    for i in arr:
        if j == 0:
            res = i
        else:
            res = res + i[0].upper() + i[1:]
        j += 1
    return res


def to_pascal_case(text):
    arr = filter(None, text.lower().split('_'))
    res = ''
    j = 0
    for i in arr:
        res = res + i[0].upper() + i[1:]
        j += 1
    return res


def camel_to_underline(camel_format):
    """
    驼峰命名格式转下划线命名格式
    :param camel_format:
    :return:
    """
    underline_format = ''
    is_first = True
    if isinstance(camel_format, str):
        for _s_ in camel_format:
            if is_first:
                underline_format += _s_ if not _s_.isupper() else _s_.lower()
                is_first = False
            else:
                underline_format += _s_ if not _s_.isupper() else '_' + _s_.lower()
    return underline_format
