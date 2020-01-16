# -*- coding: utf-8 -*-
import datetime
import os

from sqlalchemy import desc

from {{cookiecutter.app_name}}.commons.constants import const
from {{cookiecutter.app_name}}.commons.constants.const import IS_VALID_Y
from {{cookiecutter.app_name}}.models import DictItem
from {{cookiecutter.app_name}}.extensions import db


def get_dict_list(dict_code):
    """
    获取字典列表
    :param dict_code:
    :return:
    """
    if dict_code:
        return DictItem.query.filter_by(dict_code=dict_code, is_valid=IS_VALID_Y).all()
    else:
        return None


def get_dict_map(dict_code):
    """
    获取字典映射
    :param dict_code:
    :return: dict
    """
    if dict_code:
        dicts = DictItem.query.filter_by(dict_code=dict_code, is_valid=IS_VALID_Y).all()
        return {it.item_code: it.item_name for it in dicts}
    else:
        return {}


def get_revert_dict_map(dict_code):
    """
    获取反向字典映射
    :param dict_code:
    :return: dict
    """
    if dict_code:
        dicts = DictItem.query.filter_by(dict_code=dict_code, is_valid=IS_VALID_Y).all()
        return {it.item_name: it.item_code for it in dicts}
    else:
        return {}

def get_curr_mon_fir():
    """
    获取本周的周一和周5日期
    :return:
    """
    today = datetime.date.today()
    today_weekday = today.weekday()
    mon = today - datetime.timedelta(today_weekday)
    fri = today + datetime.timedelta(4 - today_weekday) if today_weekday <= 4 else today - datetime.timedelta(6 - today_weekday)
    fri += datetime.timedelta(days=7)
    return mon, fri

def get_next_mon_sun():
    """
    获取下周一和下周日
    :return:
    """
    today = datetime.date.today()
    today_weekday = today.weekday()
    next_mon = today + datetime.timedelta(6 - today_weekday + 1)
    next_sun = next_mon + datetime.timedelta(6)
    return next_mon, next_sun


def get_next_next_mon_sun():
    """
    获取下下周一和下下周日
    :return:
    """
    today = datetime.date.today()
    today_weekday = today.weekday()
    next_next_mon = today + datetime.timedelta(6 - today_weekday + 1 + 7)
    next_next_sun = next_next_mon + datetime.timedelta(6)
    return next_next_mon, next_next_sun

def trim_all_columns(df):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)
