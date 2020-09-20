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

from reader.api.controller import json_response, log_request
from reader.base.constant import ResponseCode
from reader.base.models import FeedModel
from reader.service.feeds import FeedService
from reader.util.logger import logger
from reader.util.validator import RequestValidator


class AddFeedsView(View):

    @staticmethod
    @json_response
    @log_request
    def post(request):

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
        return {
            "code": ResponseCode.SUCCESS,
            "data": result,
            "message": "获取成功!"
        }


class UpdateFeedView(View):
    @staticmethod
    @json_response
    @log_request
    def post(request):
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
            obj: FeedModel = FeedModel.instance.update_feed_by_id(
                params.get("feedId"),
                name=params.get("name"),
                description=params.get("description"),
                feed_url=params.get("feedUrl"),
                interval=params.get("interval"),
                enabled=params.get("enabled"),
            )
            if not obj:
                logger.error("update feed failed.")
                return {"code": ResponseCode.ERROR_DB, "message": "update feed failed."}
            else:
                data = obj.convert()
                return {"code": ResponseCode.SUCCESS, "message": "Update success.", "data": data}


class DeleteFeedView(View):

    @json_response
    @log_request
    def post(self, request):

        check_result = RequestValidator.check(request, {
            "feedId": {"empty": True, "type": int},
        }, RequestValidator.Methods.POST_JSON)
        if check_result.error:
            msg = check_result.error_message
            logger.error(f"error: {msg}")
            return {"code": ResponseCode.ERROR_PARAMS, "message": msg}

        params = check_result.params

        if not FeedModel.instance.get_feed_by_id(params.get("feedId")):
            return {"code": ResponseCode.ERROR_PARAMS, "message": "feedId不存在!"}

        obj = FeedModel.instance.delete_feed_by_id(params.get("feedId"))
        if obj:
            return {"code": ResponseCode.SUCCESS, "message": "删除成功."}


class SwitchFeedEnabledView(View):
    @json_response
    @log_request
    def post(self, request):

        check_result = RequestValidator.check(request, {
            "feedId": {"empty": True, "type": int},
        }, RequestValidator.Methods.POST_JSON)
        if check_result.error:
            msg = check_result.error_message
            logger.error(f"error: {msg}")
            return {"code": ResponseCode.ERROR_PARAMS, "message": msg}

        params = check_result.params

        obj = FeedModel.instance.switch_feed_enabled_by_id(params.get("feedId"))
        if obj:
            return {"code": ResponseCode.SUCCESS, "message": "切换成功.", "data": obj.convert()}
        else:
            return {"code": ResponseCode.ERROR_DB, "message": "切换失败."}


class GetFeedDetailByIdView(View):
    service = FeedService()

    @json_response
    @log_request
    def get(self, request):
        result = self.service.get_detail_by_id(request)
        obj = result.get("obj")
        if obj:
            return {"code": ResponseCode.SUCCESS, "message": "获取成功", "data": obj.convert()}
        else:
            # error
            check_result = result.get("check_result")
            if check_result.error:
                return {"code": ResponseCode.ERROR_PARAMS, "message": check_result.error_message}
            else:
                return {"code": ResponseCode.ERROR_DB, "message": "ID不存在."}
