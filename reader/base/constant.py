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
