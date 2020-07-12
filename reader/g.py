#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    g
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    全局变量存放 application_context
    因为加了类型注解，会出现循环引用的情况，因此使用全局变量中转一下

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
application_context = None
