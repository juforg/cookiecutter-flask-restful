# -*- coding: utf-8 -*-
# @author: songjie
# @email: songjie@shanshu.ai
# @date: 2020/03/03
import logging


class CustomAdapter(logging.LoggerAdapter):
    """
    This example adapter expects the passed in dict-like object to have a
    'connid' key, whose value in brackets is prepended to the log message.
    """

    def process(self, msg, kwargs):
        return '[%s] %s' % (self.extra['connid'], msg), kwargs
