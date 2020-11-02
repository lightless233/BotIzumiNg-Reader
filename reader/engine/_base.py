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
import asyncio
import multiprocessing
import threading
from typing import Optional

from reader.base.constant import EngineStatus


class CommonBaseEngine(object):

    def __init__(self):
        super(CommonBaseEngine, self).__init__()

        self.name = "_base_engine_"
        self.status = EngineStatus.READY

        self.application = self.application_context = None

    def set_application_context(self, application):
        self.application = self.application_context = application

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


class CoPoolEngine(CommonBaseEngine):

    def __init__(self, name, pool_size=None):
        super(CoPoolEngine, self).__init__()
        self.name = name

        self.co_wrapper_thread: Optional[threading.Thread] = None
        self.loop = None

        self.event: Optional[asyncio.Event] = None

        self.pool_size = pool_size if pool_size else multiprocessing.cpu_count() * 2 + 1

    def start(self):
        self.status = EngineStatus.RUNNING
        self.co_wrapper_thread = threading.Thread(target=self.__wrapper, name=self.name)
        self.co_wrapper_thread.start()

    def stop(self):
        self.status = EngineStatus.STOP
        self.event.set()

    def is_alive(self):
        return self.co_wrapper_thread.is_alive()

    def _init_event(self):
        self.event = asyncio.Event()

    async def _wait(self, timeout: float):
        try:
            await asyncio.wait_for(self.event.wait(), timeout)
        except asyncio.TimeoutError:
            pass
        finally:
            return self.event.is_set()

    def __wrapper(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(asyncio.gather(*[self._worker(idx) for idx in range(self.pool_size)]))

    @abc.abstractmethod
    async def _worker(self, idx):
        pass


class ThreadEngine(CommonBaseEngine):

    def __init__(self, name):
        super(ThreadEngine, self).__init__()

        self.name = name
        self.worker_thread: Optional[threading.Thread] = None
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
