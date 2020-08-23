#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    validator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import json
from typing import Dict, Optional

from django.http import HttpRequest


class RequestValidator:
    class Result:
        def __init__(self):
            self.error: Optional[bool] = None
            self.error_message: Optional[str] = None
            self.params: dict = {}

    class Methods:
        POST_JSON = 1
        GET_DATA = 2
        POST_DATA = 3

    @classmethod
    def check(cls, request: HttpRequest, params: Dict, method=Methods.POST_DATA) -> Result:
        """
        params: {
            "param_name_1": {empty, type, validate_function},
            "param_name_2": {empty},    // 检查变量的值是否为空，None 或 ""
            "param_name_3": {},
            "param_name_4": None,
        }

        :param request:
        :param params:
        :param method:
        :return:
        """
        result = RequestValidator.Result()
        if method == cls.Methods.POST_DATA:
            request_data = request.POST
        elif method == cls.Methods.POST_JSON:
            request_data = json.loads(request.body)
        elif method == cls.Methods.GET_DATA:
            request_data = request.GET
        else:
            result.error_message = "Unknown check method."
            result.error = True
            return result

        # start validate
        request_keys = request_data.keys()
        checks: Optional[Dict]
        for expect_key, checks in params.items():
            # check if the expected key has be sent
            if expect_key not in request_keys:
                result.error_message = "'{}' not exist.".format(expect_key)
                result.error = True
                return result

            # check validator
            if checks is None or len(checks) == 0:
                result.params[expect_key] = request_data.get(expect_key)
                continue

            req_value = request_data.get(expect_key, None)
            if checks.get("empty") and (req_value is None or req_value == ""):
                result.error_message = "'{}' is empty.".format(expect_key)
                result.error = True
                return result

            expect_type = checks.get("type")
            if expect_type and not isinstance(req_value, expect_type):
                result.error_message = "'{}' require type {}, but type {} found.".format(
                    expect_key, expect_type, type(req_value)
                )
                result.error = True
                return result

            validate_func = checks.get("validate_function")
            if validate_func:
                tmp: Optional[Dict] = validate_func(req_value)
                if tmp is not None and tmp.get("error"):
                    result.error_message = tmp.get("error_message")
                    result.error = True
                    return result

            result.params[expect_key] = request_data.get(expect_key)

        result.error = False
        return result
