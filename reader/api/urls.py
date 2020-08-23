#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    urls
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""

from django.urls import path

from reader.api.controller import feeds

urlpatterns = [
    path("v1/feed/add", feeds.AddFeedsView.as_view())
]
