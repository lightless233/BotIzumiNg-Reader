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

import aiohttp

from reader import g
from reader.engine._base import CoPoolEngine
from reader.util.logger import logger


class FetcherEngine(CoPoolEngine):

    def __init__(self, name, pool_size=None):
        super(FetcherEngine, self).__init__(name, pool_size)

        self.feed_task_queue: queue.Queue = g.queue_context.feed_task_queue
        self.parser_task_queue: queue.Queue = g.queue_context.parser_task_queue

        self.client_timeout = aiohttp.ClientTimeout(total=60, connect=12, sock_read=12, sock_connect=12)

    async def _worker(self, idx):
        self._init_event()
        cur_name = f"{self.name}-{idx}"
        logger.info(f"{cur_name} start.")

        while self.is_running():
            try:
                task = self.feed_task_queue.get_nowait()
                logger.debug(f"get task: {task}")

                # 从 task 中获取 feed_url
                feed_url = task.get("feed_url")
                if not feed_url:
                    logger.warning(f"{cur_name} empty feed_url!")
                    await self._wait(1)
                    continue

                # 发起请求
                async with aiohttp.request("GET", feed_url, timeout=self.client_timeout) as resp:
                    if resp.status != 200:
                        logger.warning(
                            f"{cur_name} Error while making request to {feed_url}, status code: {resp.status}")
                        # TODO 更新 feed 的状态到 dead
                        await self._wait(1)
                        continue

                    # status code 是 200 的情况
                    content = await resp.text()
                    parser_task = {
                        "feed_task": task,
                        "content": content,
                    }
                    while self.is_running():
                        try:
                            self.parser_task_queue.put_nowait(parser_task)
                        except queue.Full:
                            logger.warning(f"{cur_name} parser task queue full, retry..")
                            await self._wait(1)
                        else:
                            break

                    logger.debug(f"{cur_name} content size: {len(content)}")

            except queue.Empty:
                await self._wait(1)
                continue

        logger.info(f"{cur_name} stop.")
