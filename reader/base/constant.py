#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    constant
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from dataclasses import dataclass


@dataclass
class EngineStatus:
    READY = 0x00
    RUNNING = 0x01
    STOP = 0x02


@dataclass
class FeedsStatus:
    # 0-待更新，1-更新中，2-存活，3-已死亡
    TOBE_UPDATE = 0
    UPDATING = 1
    ALIVE = 2
    DEAD = 3


class ResponseCode:
    SUCCESS = 2000

    UNKNOWN_ERROR = 4000
    ERROR_PARAMS = 4001
    ERROR_DB = 4002
    ERROR_RUNTIME = 4003


TIME_FORMAT_STRING = "%Y-%m-%d %H:%M:%S"
