# -*- coding: utf-8 -*-
#
# #  Copyright (c) ©2019, Cardinal Operations and/or its affiliates. All rights reserved.
# #  CARDINAL OPERATIONS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
# # @author: songjie@shanshu.ai
# # @date: 2019/09/25
from pandas import DataFrame

from {{cookiecutter.app_name}}.extensions import redis_client
import pickle

DEFAULT_EX = 3600 * 24

def cache_df(key, data_df,ex= DEFAULT_EX):
    """
    通用缓存dataframe 用的方法
    :param ex: 过期时间，默认1天过期
    :param data_df:
    :param key:
    :return:
    """
    if data_df is None:
        return False
    if isinstance(data_df,DataFrame):
        if not data_df.empty:
            return redis_client.set(key, pickle.dumps(data_df),ex=ex)
    else:
        return redis_client.set(key, pickle.dumps(data_df), ex=ex)
    return False

def get_df_from_cache(key):
    """
    获取缓存的dataframe
    :param key:
    :return: dataframe
    """
    pickle_data = redis_client.get(key)
    if pickle_data is None:
        return None
    else:
        return pickle.loads(pickle_data)

def expire_all_caches():
    """
    使所有缓存过期
    :return:
    """

    # 1. 获取所有符合规则的key TODO
    # redis_client.expire
    #2. 逐个删除key

    pass

def expire_key(key):
    """
    删除可以
    :param key:
    :return:
    """
    redis_client.delete(key)