#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    cors_middleware
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from typing import List
from urllib.parse import urlparse

from django.conf import settings
from django.http import HttpResponseForbidden

from reader.util.logger import logger


class CORSMiddleware:

    def __init__(self, get_response):
        super(CORSMiddleware, self).__init__()
        self.get_response = get_response
        try:
            self.allowed_origins: List[str] = settings.ALLOWED_ORIGINS
        except AttributeError:
            logger.error("请在配置文件中配置 'ALLOWED_ORIGIN' 选项")
            self.allowed_origins: List[str] = []

    def __call__(self, request):
        origin: str = request.META.get("HTTP_ORIGIN", None)
        response = self.get_response(request)

        if origin:
            o = urlparse(origin)
            if o.hostname in self.allowed_origins:
                response["Access-Control-Allow-Origin"] = origin
                response["Access-Control-Allow-Headers"] = "Content-Type, X-CSRFToken, X-ReaderToken"
                response["Access-Control-Allow-Credentials"] = "true"
                response["Access-Control-Expose-Headers"] = "X-ReaderToken"
                return response
            else:
                return HttpResponseForbidden("invalid origin")
        return response
