#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    engine_context
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from typing import Optional

from reader.engine import FetcherEngine, RefreshEngine


class ApplicationEngineContext(object):

    def __init__(self):
        super(ApplicationEngineContext, self).__init__()
        self.refresh_engine: Optional[RefreshEngine] = None
        self.fetcher_engine: Optional[FetcherEngine] = None

    def init_engines(self):
        self.refresh_engine = RefreshEngine("refresh_engine")
        self.refresh_engine.start()

        self.fetcher_engine = FetcherEngine("fetcher_engine")
        self.fetcher_engine.start()

    def stop_engines(self):
        self.refresh_engine.stop()
        self.fetcher_engine.stop()
