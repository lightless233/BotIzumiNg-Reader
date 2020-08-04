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

from reader.engine import FetcherEngine, RefreshEngine, ParserEngine, SaveEngine


class ApplicationEngineContext(object):

    def __init__(self):
        super(ApplicationEngineContext, self).__init__()
        self.refresh_engine: Optional[RefreshEngine] = None
        self.fetcher_engine: Optional[FetcherEngine] = None
        self.parser_engine: Optional[ParserEngine] = None
        self.save_engine: Optional[SaveEngine] = None

    def init_engines(self):
        """启动的时候应该从最后的 engine 开始启动"""
        # TODO: fix order
        self.refresh_engine = RefreshEngine("refresh_engine")
        self.refresh_engine.start()

        self.fetcher_engine = FetcherEngine("fetcher_engine")
        self.fetcher_engine.start()

        self.parser_engine = ParserEngine("parser_engine")
        self.parser_engine.start()

        self.save_engine = SaveEngine("save_engine")
        self.save_engine.start()

    def stop_engines(self):
        """结束的时候从最前的 engine 开始结束"""
        self.refresh_engine.stop()
        self.fetcher_engine.stop()
        self.parser_engine.stop()
        self.save_engine.stop()
