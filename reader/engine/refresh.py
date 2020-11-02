#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    refresh.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import datetime
import queue

from reader.base.constant import FeedStatus
from reader.base.models.feed import FeedModel
from reader.engine._base import ThreadEngine
from reader.util.logger import logger


class RefreshEngine(ThreadEngine):
    def __init__(self, name):
        super(RefreshEngine, self).__init__(name)
        self.refresh_interval = 30

    def put_to_queue(self, q: queue.Queue, task):
        retry_timeout = 3
        while True:
            try:
                q.put_nowait(task)
                break
            except queue.Full:
                logger.warning("queue is full, retry in 3s.")
                self.thread_event.wait(retry_timeout)

    def _worker(self):

        logger.info(f"{self.name} start!")
        task_queue = self.application.queues.feed_task_queue

        while self.is_running():

            # 从db中找到所有的待刷新的 feed 源
            row: FeedModel
            for row in FeedModel.instance.all():
                logger.debug(f"name: {row.name} ,last_refresh_time: {row.last_refresh_time}")
                if row.last_refresh_time + datetime.timedelta(minutes=row.interval) > datetime.datetime.now():
                    continue

                # add to queue
                task = {
                    "id": row.id,
                    "name": row.name,
                    "feed_url": row.feed_url,
                }
                self.put_to_queue(task_queue, task)
                logger.debug(f"put task {task} to queue.")

                # update last_refresh_time
                row.last_refresh_time = datetime.datetime.now()
                row.status = FeedStatus.UPDATING
                row.save()

            # wait for next wakeup
            self.thread_event.wait(self.refresh_interval)

        logger.info(f"{self.name} stop!")
