#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    __init__.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from functools import wraps

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse

from reader.util.logger import logger


def json_response(view_func):
    @wraps(view_func)
    def _wrap(*args, **kwargs):
        r = view_func(*args, **kwargs)
        return JsonResponse(r)

    return _wrap


def log_request(view_func):
    @wraps(view_func)
    def _wrap(*args, **kwargs):
        request = None

        for arg in args:
            if isinstance(arg, WSGIRequest):
                request = arg
                break

        if request is not None:
            logger.debug("URI: {}, POST: {}".format(request.path, request.body))
        else:
            logger.warning("无法获取 request 实例.")
        return view_func(*args, **kwargs)

    return _wrap
