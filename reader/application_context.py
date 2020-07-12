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

from reader.util.logger import logger


class ApplicationContext(object):
    class Queues:
        feed_task_queue: queue.Queue

    def __init__(self):
        super(ApplicationContext, self).__init__()

        self.init_queues()
        logger.info("Init queues done.")

    def init_queues(self):
        self.Queues.feed_task_queue = queue.Queue(maxsize=16)


application_context = ApplicationContext()
