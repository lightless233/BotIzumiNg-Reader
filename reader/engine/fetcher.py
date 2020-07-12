#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    fetcher
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    fetcher engine

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import queue

from reader import g
from reader.engine._base import CoPoolEngine
from reader.util.logger import logger


class FetcherEngine(CoPoolEngine):

    def __init__(self, name, pool_size=None):
        super(FetcherEngine, self).__init__(name, pool_size)

        self.feed_task_queue: queue.Queue = g.queue_context.feed_task_queue

    async def _worker(self, idx):
        self._init_event()
        cur_name = f"{self.name}-{idx}"
        logger.info(f"{cur_name} start.")

        while self.is_running():
            try:
                task = self.feed_task_queue.get_nowait()
                logger.debug(f"get task: {task}")
            except queue.Empty:
                await self._wait(3)
                continue

        logger.info(f"{cur_name} stop.")
