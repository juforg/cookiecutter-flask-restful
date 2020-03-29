# -*- coding: utf-8 -*-

#  Copyright (c) ©2019, Cardinal Operations and/or its affiliates. All rights reserved.
#  CARDINAL OPERATIONS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

# @author: songjie@shanshu.ai
# @date: 2019/09/24
import copy


class BizException(Exception):
    def __init__(
            self, msg, data=None
    ):
        self.data = data
        self.msg = msg
        super().__init__(msg)


class C(Exception):
    __code: str
    __msg: str
    __data: object

    def __init__(self, code, msg):
        self.__code = code
        self.__msg = msg

    def f(self, *args, **kwargs):
        """
        必须通过此方式格式化，否则会导致 别的没办法格式化了
        :param args:
        :param kwargs:
        :return:
        """
        res = copy.copy(self)
        res.__msg = res.__msg.format(*args)
        super(C, res).__init__(f"{res.__code}:{res.__msg}")
        return res

    @property
    def code(self):
        return self.__code

    @property
    def msg(self):
        return self.__msg

    @__data.setter
    def data(self, value):
        res = copy.copy(self)
        res.__data = value
        return res

    @property
    def dict(self):
        if self.__data:
            return {"code": self.__code, "msg": self.__msg, "data": self.__data}
        else:
            return {"code": self.__code, "msg": self.__msg}
