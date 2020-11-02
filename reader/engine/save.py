#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    save
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    save engine

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import hashlib
import queue

from reader.base.models import PaperModel
from reader.engine._base import ThreadEngine
from reader.util.logger import logger


class SaveEngine(ThreadEngine):
    def __init__(self, name):
        super(SaveEngine, self).__init__(name)

    def _worker(self):
        logger.info(f"{self.name} start!")

        self.save_queue = self.application.queues.save_task_queue

        while self.is_running():
            try:
                task = self.save_queue.get_nowait()
            except queue.Empty:
                self.thread_event.wait(1)
                continue

            feed_id = task.get("feed_task").get("id")
            title: str = task.get("title")
            content: str = task.get("content")
            link = task.get("link")
            unique_hash = "{}|{}".format(
                hashlib.md5(title.encode()).hexdigest(),
                hashlib.md5(content.encode()).hexdigest()
            )
            tags = task.get("tags")
            publish_time = task.get("publish_time")

            # 根据 unique_hash 来决定这个 paper 是否已经存在了
            # TODO 这里需要考虑文章更新的情况
            if PaperModel.instance.get_paper_by_unique_hash(unique_hash):
                continue
            else:
                paper = PaperModel(feed_id=feed_id, title=title, content=content, link=link, unique_hash=unique_hash,
                                   tags=tags, pushed_status=0, publish_time=publish_time)
                paper.save()
                logger.debug(f"{self.name} paper saved, title: {title}, unique_hash: {unique_hash}")

        logger.info(f"{self.name} stop!")
