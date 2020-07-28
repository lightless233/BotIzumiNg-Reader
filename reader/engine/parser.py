#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    parser
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    parser xml

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import queue
from datetime import datetime, timezone, timedelta
from time import mktime

import feedparser
from pytz import utc

from reader import g
from reader.engine._base import ThreadEngine
from reader.util.logger import logger


class ParserEngine(ThreadEngine):

    def __init__(self, name):
        super(ParserEngine, self).__init__(name)

        self.parser_task_queue: queue.Queue = g.queue_context.parser_task_queue

    def _worker(self):
        # 有两种格式，需要分别做解析
        # rss20 -> "https://paper.seebug.org/rss/"
        # atom10 -> "http://wiki.ioin.in/atom"

        while self.is_running():

            try:
                task = self.parser_task_queue.get_nowait()
            except queue.Empty:
                self.thread_event.wait(1)
                continue

            feed_content = task.get("content")
            if feed_content is None:
                continue

            fd = feedparser.parse(feed_content)
            fd_version = fd.version

            if fd_version == "rss20":
                self.__parse_rss20(fd)
            elif fd_version == "atom10":
                self.__parse_atom10(fd)
            else:
                logger.error(f"{self.name} unknown fd_version: {fd_version}")
                continue

    @staticmethod
    def __parse_rss20(fd):
        entries = fd.entries
        entry: feedparser.FeedParserDict
        for entry in entries:
            title = entry.get("title")
            link = entry.get("link")
            summary = entry.get("summary")
            summary = summary[:128] if len(summary) > 128 else summary
            published_time_struct = entry.get("published_parsed")

            # todo deal with struct time
            dt = datetime.fromtimestamp(mktime(published_time_struct))
            dt = dt.astimezone(timezone(timedelta(hours=8)))

    def __parse_atom10(self, fd):
        pass
