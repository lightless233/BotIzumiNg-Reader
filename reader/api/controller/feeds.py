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
import time
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
            feed_url=params.get("feedUrl"),
            interval=params.get("interval"),
            status=0,
            health_status=0,
            enabled=0,
            last_refresh_time=datetime.now(),
            author=1,  # TODO: author 字段先保留
            created_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        if obj:
            return {"code": ResponseCode.SUCCESS, "message": "添加成功!", "data": obj.convert()}
            # return {
            #     "code": ResponseCode.SUCCESS,
            #     "message": "添加成功!",
            #     "data": {
            #         "id": obj.id,
            #         "feedName": obj.name,
            #         "description": obj.description,
            #         "feedUrl": obj.feed_url,
            #         "interval": int(obj.interval),
            #         "status": int(obj.status),
            #         "healthStatus": int(obj.health_status),
            #         "enabled": int(obj.enabled),
            #         "lastRefreshTime": obj.last_refresh_time.strftime(TIME_FORMAT_STRING),
            #         "author": obj.author,
            #     }
            # }
        else:
            return {
                "code": ResponseCode.ERROR_DB,
                "message": "添加失败!",
            }


class ListFeedView(View):
    @staticmethod
    @json_response
    def get(request):
        result = []
        objs = FeedModel.instance.all()
        for obj in objs:
            result.append(obj.convert())
            # result.append({
            #     "id": obj.id,
            #     "feedName": obj.name,
            #     "description": obj.description,
            #     "feedUrl": obj.feed_url,
            #     "interval": int(obj.interval),
            #     "status": int(obj.status),
            #     "healthStatus": int(obj.health_status),
            #     "enabled": int(obj.enabled),
            #     "lastRefreshTime": obj.last_refresh_time.strftime(TIME_FORMAT_STRING),
            #     "author": obj.author,
            # })
        # time.sleep(10)
        return {
            "code": ResponseCode.SUCCESS,
            "data": result,
            "message": "获取成功!"
        }


class UpdateFeedView(View):
    @staticmethod
    @json_response
    def post(request):
        logger.debug("POST: {}".format(request.body))

        check_result = RequestValidator.check(request, {
            "feedId": {"empty": True, "type": int},
            "name": {"empty": True},
            "description": {"empty": True},
            "feedUrl": {"empty": True},
            "interval": {"empty": True, "type": int},
            "enabled": {"empty": True, "type": int},
        }, RequestValidator.Methods.POST_JSON)

        if check_result.error:
            m = check_result.error_message
            logger.error("error: {}".format(m))
            return {"code": ResponseCode.ERROR_PARAMS, "message": m}
        
        params = check_result.params
        
        if not FeedModel.instance.get_feed_by_id(params.get("feedId")):
            return {"code": ResponseCode.ERROR_PARAMS, "message": "feedId不存在!"}
        else:
            obj: FeedModel = FeedModel.instance.update_feed_by_id(params.get("feedId"), 
                name=kwargs.get("name"),
                description=kwargs.get("description"),
                feed_url=kwargs.get("feed_url"),
                interval=kwargs.get("interval"),
                enabled=kwargs.get("enabled"),
            )
            if not obj:
                logger.error("update feed failed.")
                return {"code": ResponseCode.ERROR_DB, "message": "update feed failed."}
            else:
                data = obj.convert()
                return {"code": ResponseCode.SUCCESS, "message": "Update success.", "data": data};


class DeleteFeedView(View):
    @staticmethod
    @json_response
    def post(request):
        logger.debug("POST: {}".format(request.body))

        check_result = RequestValidator.check(request, {
            "feedId": {"empty": True, "type": int},
        }, RequestValidator.Methods.POST_JSON)
        if check_result.error:
            msg = check_result.error_message
            logger.error("error: {}".format(msg))
            return {"code": ResponseCode.ERROR_PARAMS, "message": msg}
        
        params = check_result.params

        if not FeedModel.instance.get_feed_by_id(params.get("feedId")):
            return {"code": ResponseCode.ERROR_PARAMS, "message": "feedId不存在!"}
        
        obj = FeedModel.instance.delete_feed_by_id(feed_id)
        if obj:
            return {"code": ResponseCode.SUCCESS, "message": "Delete success.", "data": obj.convert()}


class SwitchFeedEnabledView(View):
    @staticmethod
    @json_response
    def post(request):
        logger.debug("POST: {}".format(request.body))

        check_result = RequestValidator.check(request, {
            "feedId": {"empty": True, "type": int},
        }, RequestValidator.Methods.POST_JSON)
        if check_result.error:
            msg = check_result.error_message
            logger.error("error: {}".format(msg))
            return {"code": ResponseCode.ERROR_PARAMS, "message": msg}
        
        params = check_result.params

        obj = FeedModel.instance.switch_feed_enabled_by_id(params.get("feedId"))
        if obj:
            return {"code": ResponseCode.SUCCESS, "message": "切换成功.", "data": obj.convert()}
        else:
            return {"code": ResponseCode.ERROR_DB, "message": "切换失败."}
