# -*- coding: utf-8 -*-
# @author: songjie
# @email: songjie@shanshu.ai
# @date: 2020/03/03
import logging
import threading


class CustomAdapter(logging.LoggerAdapter):
    """
    This example adapter expects the passed in dict-like object to have a
    'connid' key, whose value in brackets is prepended to the log message.
    """

    def process(self, msg, kwargs):
        return '[%s] %s' % (self.extra['connid'], msg), kwargs


class CustomLogger(logging.Logger):

    def _log(self, level, msg, args, exc_info=None, extra=None):
        local_values = threading.local()
        if hasattr(local_values, "cust_log_tag"):
            cust_log_tag = local_values.cust_log_tag
        else:
            cust_log_tag = {"trace_id": 'tid'}
        if extra is None:
            extra = cust_log_tag
        else:
            extra.update(cust_log_tag)
        super(CustomLogger, self)._log(level, msg, args, exc_info, extra)
