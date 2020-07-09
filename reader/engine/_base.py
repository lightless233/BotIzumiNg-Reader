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
    def start(self):
        raise NotImplementedError
