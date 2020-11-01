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
import signal

from reader import g
from reader.context.engine_context import ApplicationEngineContext
from reader.context.queue_context import ApplicationQueueContext
from reader.util.logger import logger


class Application(object):

    def __init__(self):
        super(Application, self).__init__()

        g.queue_context = self.queues = ApplicationQueueContext()
        self.engines = ApplicationEngineContext()

        self._engines = {}

    def start(self):
        signal.signal(signal.SIGINT, self.__sigint)
        logger.info("exit process register done.")

        self.init_queues()
        logger.info("Init queues done.")

        self.init_engines()
        logger.info("Init engines done.")

    def register_engine(self, engine):
        """
        注册 engine 的接口
        :param engine:
        :return:
        """
        instance = engine(self)
        name = instance.name
        self._engines[name] = instance

    def init_queues(self):
        self.queues.init_queues()

    def init_engines(self):
        self.engines.init_engines()

    def __sigint(self, sig, frame):
        logger.info("Receive exit signal.")
        self.engines.stop_engines()
