#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    parser
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    parser xml

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from reader.engine._base import ThreadEngine


class ParserEngine(ThreadEngine):
    def __init__(self, name):
        super(ParserEngine, self).__init__(name)

    def _worker(self):
        # 有两种格式，需要分别做解析
        # rss20 -> "https://paper.seebug.org/rss/"
        # atom10 -> "http://wiki.ioin.in/atom"
        pass
