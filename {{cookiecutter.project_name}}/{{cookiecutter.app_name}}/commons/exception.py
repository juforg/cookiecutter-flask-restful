# -*- coding: utf-8 -*-

#  Copyright (c) ©2019, Cardinal Operations and/or its affiliates. All rights reserved.
#  CARDINAL OPERATIONS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

# @author: songjie@shanshu.ai
# @date: 2019/09/24


class BizException(Exception):
    def __init__(
            self,  msg, data = None
    ):
        self.data = data
        self.msg = msg
        super().__init__(msg)
