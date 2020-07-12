#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    _base.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import abc
import threading

from reader.base.constant import EngineStatus


class CommonBaseEngine(object):

    def __init__(self):
        super(CommonBaseEngine, self).__init__()

        self.name = "_base_engine_"
        self.status = EngineStatus.READY

    def is_running(self):
        return self.status == EngineStatus.RUNNING

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass

    @abc.abstractmethod
    def is_alive(self):
        pass


class CoEngine(CommonBaseEngine):
    # def start(self):
    #     raise NotImplementedError
    #
    # def stop(self):
    #     raise NotImplementedError
    #
    # def is_alive(self):
    #     raise NotImplementedError

    @abc.abstractmethod
    async def _worker(self, idx):
        pass


class ThreadEngine(CommonBaseEngine):

    def __init__(self, name):
        super(ThreadEngine, self).__init__()

        self.name = name
        self.worker_thread: threading.Thread
        self.thread_event: threading.Event = threading.Event()

    def start(self):
        self.status = EngineStatus.RUNNING
        self.worker_thread = threading.Thread(target=self._worker, name=self.name)
        self.worker_thread.start()

    def stop(self):
        self.status = EngineStatus.STOP
        self.thread_event.set()

    def is_alive(self):
        return self.worker_thread.is_alive()

    @abc.abstractmethod
    def _worker(self):
        pass
