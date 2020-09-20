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
    path("v1/feed/add", feeds.AddFeedsView.as_view()),
    path("v1/feed/list", feeds.ListFeedView.as_view()),
    path("v1/feed/update", feeds.UpdateFeedView.as_view()),
    path("v1/feed/delete", feeds.DeleteFeedView.as_view()),
    path("v1/feed/switch_enabled", feeds.SwitchFeedEnabledView.as_view()),
]
