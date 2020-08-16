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

import feedparser
import jieba.analyse

from reader import g
from reader.engine._base import ThreadEngine
from reader.util.logger import logger


class ParserEngine(ThreadEngine):

    def __init__(self, name):
        super(ParserEngine, self).__init__(name)

        self.parser_task_queue: queue.Queue = g.queue_context.parser_task_queue
        self.save_queue: queue.Queue = g.queue_context.save_task_queue

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
                logger.debug(f"{self.name} use rss20 parser.")
                save_tasks = self.__parse_rss20(fd)
            elif fd_version == "atom10":
                logger.debug(f"{self.name} use atom10 parser.")
                save_tasks = self.__parse_atom10(fd)
            else:
                logger.error(f"{self.name} unknown fd_version: {fd_version}")
                continue

            for save_task in save_tasks:
                # put `feed_task` to save task
                save_task["feed_task"] = task.get("feed_task")

                # extract tags from summary
                save_task["tags"] = jieba.analyse.extract_tags(save_task["content"], topK=5)

                # put save task to queue
                while self.is_running():
                    try:
                        self.save_queue.put_nowait(save_task)
                        self.thread_event.wait(1)
                    except queue.Full:
                        logger.warning(f"{self.name} save_queue full, retry...")
                        continue
                    else:
                        break

    @staticmethod
    def __parse_rss20(fd):
        entries = fd.entries
        entry: feedparser.FeedParserDict
        save_tasks = []

        for entry in entries:
            title = entry.get("title")
            link = entry.get("link")
            summary = entry.get("summary")
            # st_time = entry.get("published_parsed")
            time_string = entry.get("published")

            # st_time have no timezone info, just convert it to UTC+8
            # use arrow lib:
            #   atime = arrow.get(st_time)
            #   atime = atime.astimezone(tz.gettz("Asia/Shanghai"))
            # or use python lib (FUCKING PYTHON LIB):
            # dt = datetime.fromtimestamp(timegm(st_time))
            # dt = dt.astimezone(timezone(timedelta(hours=8)))
            # logger.debug(f"title: {title}, st_time: {st_time}, time_string: {time_string}, dt: {dt}")

            # TODO: add to save queue
            save_task = {
                "title": title,
                "content": summary,
                "publish_time": time_string,
                "link": link
            }

            save_tasks.append(save_task)

        return save_tasks

    @staticmethod
    def __parse_atom10(fd):
        entries = fd.entries
        entry: feedparser.FeedParserDict
        save_tasks = []

        for entry in entries:
            title = entry.get("title")
            link = entry.get("link")
            summary = entry.get("summary")
            time_string = entry.get("updated")

            # TODO: add to save queue
            save_task = {
                "title": title,
                "content": summary,
                "publish_time": time_string,
                "link": link
            }

            save_tasks.append(save_task)
        return save_tasks
