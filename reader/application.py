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
import collections
import signal

from reader.context.queue_context import ApplicationQueueContext
from reader.engine import SaveEngine, ParserEngine, FetcherEngine, RefreshEngine
from reader.util.logger import logger


class Application(object):

    def __init__(self):
        super(Application, self).__init__()

        self.queues = ApplicationQueueContext()

        # Python 3.6 之后，字典已经是有序的了
        # 这里还是显示的使用 OrderedDict() 兼容 3.5+
        self._engines = collections.OrderedDict()

    def start(self):
        signal.signal(signal.SIGINT, self.__sigint)
        logger.info("ExitProcess register done.")

        self.init_queues()
        logger.info("Init queues done.")

        self.init_engines()
        logger.info("Init engines done.")

    def register_engine(self, engine, name: str = None):
        """
        注册 engine 的接口
        :param name:
        :param engine:
        :return:
        """
        if name is None:
            name = engine.__name__
        instance = engine(name)
        instance.set_application_context(self)
        self._engines[name] = instance

    def init_queues(self):
        self.queues.init_queues()

    def init_engines(self):
        self.register_engine(SaveEngine)
        self.register_engine(ParserEngine)
        self.register_engine(FetcherEngine)
        self.register_engine(RefreshEngine)

        for k, v in self._engines.items():
            v.start()

    def __sigint(self, sig, frame):
        logger.info("Receive exit signal.")
        for k in list(self._engines.keys())[::-1]:
            self._engines[k].stop()


application = Application()
