# -*- coding: utf-8 -*-

#  Copyright (c) ©2019, Cardinal Operations and/or its affiliates. All rights reserved.
#  CARDINAL OPERATIONS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

# @author: songjie@shanshu.ai
# @date: 2019/09/26
import time
from threading import Thread
import os
import logging

from flask import current_app as flask_app
from celery import current_app as celery_app

logger = logging.getLogger(__name__)


class DumpData(Thread):

    def __init__(self, dir_key, **kwargs):
        super().__init__()
        self.dir_key = dir_key
        self.kwargs = kwargs
        if flask_app and flask_app.config:
            self.env = flask_app.config.get('ENV')
        elif celery_app and celery_app.conf:
            self.env = celery_app.conf.get('ENV')

    def run(self):
        if self.env == 'development':
            start = time.time()
            for (key, data_df) in self.kwargs.items():
                path = os.path.join(os.getenv("DATA_PATH", "/var/{{cookiecutter.app_name}}/data/"), self.dir_key)
                if not os.path.exists(path):
                    os.makedirs(path)
                data_df.to_csv(os.path.join(path, key + ".csv.gz"))
            logger.info("--备份数据:%s, 耗时: %s", self.dir_key, time.time() - start)