#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    application_context
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import queue
import signal

from reader.engine.refresh import RefreshEngine
from reader.util.logger import logger


class ApplicationContext(object):
    class Queues:
        feed_task_queue: queue.Queue

    class Engines:
        refresh_engine: RefreshEngine

    def __init__(self):
        super(ApplicationContext, self).__init__()

    def start(self):
        signal.signal(signal.SIGINT, self.__sigint)
        logger.info("exit process register done.")

        self.init_queues()
        logger.info("Init queues done.")

        self.init_engines()
        logger.info("Init engines done.")

    def init_queues(self):
        self.Queues.feed_task_queue = queue.Queue(maxsize=16)

    def init_engines(self):
        self.Engines.refresh_engine = RefreshEngine("refresh_engine")
        self.Engines.refresh_engine.start()

    def __sigint(self, sig, frame):
        logger.info("Receive exit signal.")
        self.Engines.refresh_engine.stop()
