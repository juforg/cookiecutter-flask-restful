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
    if str_number.isdigit() or (str_number.split('-')[-1]).isdigit():
        return True
    else:
        return False

def is_float(str_number: str):
    """
    判断字符串是否浮点
    :param str_number:
    :return:
    """
    value = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')  # 定义正则表达式
    return value.match(str_number)
