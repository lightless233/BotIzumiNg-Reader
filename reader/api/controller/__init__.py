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

from django.http import JsonResponse


def json_response(view_func):
    @wraps(view_func)
    def _wrap(*args, **kwargs):
        r = view_func(*args, **kwargs)
        return JsonResponse(r)

    return _wrap
