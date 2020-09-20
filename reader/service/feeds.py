#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    feeds
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from reader.base.models import FeedModel
from reader.service import BaseService
from reader.util.validator import RequestValidator


class FeedService(BaseService):

    def get_detail_by_id(self, request):
        check_result = RequestValidator.check(request, {
            "feedId": {"empty": True, "type": int},
        }, RequestValidator.Methods.GET_DATA)
        if check_result.error:
            return self._build_result(check_result)

        params = check_result.params
        obj = FeedModel.instance.get_feed_by_id(params.get("feedId"))
        if obj:
            return self._build_result(check_result, obj)
        else:
            return self._build_result(check_result)
