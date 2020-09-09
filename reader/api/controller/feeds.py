#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    feeds
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    feeds controller

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from datetime import datetime

from django.views import View

from reader.api.controller import json_response
from reader.base.constant import ResponseCode, TIME_FORMAT_STRING
from reader.util.logger import logger
from reader.util.validator import RequestValidator
from reader.base.models import FeedModel


class AddFeedsView(View):

    @staticmethod
    @json_response
    def post(request):
        logger.debug("POST: {}".format(request.body))

        check_result = RequestValidator.check(request, {
            "name": {"empty": True},
            "description": {"empty": True},
            "feedUrl": {"empty": True},
            "interval": {"empty": True, "type": int},
        }, RequestValidator.Methods.POST_JSON)

        if check_result.error:
            m = check_result.error_message
            logger.error("error: {}".format(m))
            return {"code": 4001, "message": m}

        params = check_result.params

        obj = FeedModel.objects.create(
            name=params.get("name"),
            description=params.get("description"),
            feed_url=params.get("feed_url"),
            interval=params.get("interval"),
            status=0,
            enabled=0,
            last_refresh_time=datetime.now(),
            author=1,  # TODO: author 字段先保留
            created_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        if obj:
            return {
                "code": 1000,
                "message": "添加成功!",
                "data": {
                    "id": obj.id,
                    "name": obj.name,
                    "description": obj.description,
                    "feed_url": obj.feed_url,
                    "interval": int(obj.interval),
                    "status": int(obj.status),
                    "enabled": int(obj.enabled),
                    "last_refresh_time": obj.last_refresh_time.strftime(TIME_FORMAT_STRING),
                    "author": obj.author,
                }
            }
        else:
            return {
                "code": ResponseCode.ERROR_DB,
                "message": "添加失败!",
            }
