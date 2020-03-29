# -*- coding: utf-8 -*-

#  Copyright (c) ©2019, Cardinal Operations and/or its affiliates. All rights reserved.
#  CARDINAL OPERATIONS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

# @author: songjie@shanshu.ai
# @date: 2019/09/26

from threading import Thread
import os
import logging

from flask import current_app

logger = logging.getLogger(__name__)


class DumpData(Thread):

    def __init__(self, dir_key, **kwargs):
        super().__init__()
        self.dir_key = dir_key
        self.kwargs = kwargs

    def run(self):
        logger.info("--备份数据:%s", self.dir_key)
        if current_app.config['ENV'] == 'development':
            for (key, data_df) in self.kwargs.items():
                if data_df is not None and not data_df.empty:
                    path = os.path.join(os.getenv("BACKUPDATA_PATH", "/var/algo/data/"), self.dir_key)
                    if not os.path.exists(path):
                        os.makedirs(path)
                    data_df.to_csv(os.path.join(path, key + ".csv"))