#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    queue_context
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import queue
from typing import Optional


class ApplicationQueueContext(object):

    def __init__(self):
        super(ApplicationQueueContext, self).__init__()

        self.feed_task_queue: Optional[queue.Queue] = None
        self.parser_task_queue: Optional[queue.Queue] = None

    def init_queues(self):
        self.feed_task_queue = queue.Queue(maxsize=16)
        self.parser_task_queue = queue.Queue(maxsize=32)
