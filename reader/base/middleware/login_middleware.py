#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    login_middleware
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    控制用户登录的中间件

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import jwt
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from reader.base.constant import AUTH_TOKEN
from reader.base.models import UserModel
from reader.util.logger import logger


class LoginCode:
    SUCCESS = 2000
    NOT_LOGIN = 4001


class LoginMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        super(LoginMiddleware, self).__init__()
        self.get_response = get_response

    def process_request(self, request):
        """
        检查 cookie 中是否有 JWT
        如果没有，就直接return
        如果有，则解码将 UUID 放到 session 中
        :param request:
        :return:
        """
        # 只有 /api/ 下面的接口才校验是否登录
        if not request.path.startswith("/api/"):
            return self.get_response(request)

        cookie_auth_token = request.COOKIES.get(AUTH_TOKEN)
        header_auth_token = request.META.get(AUTH_TOKEN)

        auth_token = cookie_auth_token if cookie_auth_token is not None else header_auth_token
        if auth_token is None:
            return JsonResponse({
                "code": LoginCode.NOT_LOGIN,
                "message": "用户未登录."
            })

        try:
            # {"id": "uuid"}
            result: dict = jwt.decode(auth_token, settings.JWT_SECRET)
            uuid = result.get("id")
        except jwt.exceptions.PyJWTError as e:
            logger.error(f"Error when decode jwt, value: {auth_token}")
            return JsonResponse({
                "code": LoginCode.NOT_LOGIN,
                "message": "用户未登录."
            })

        if uuid is None:
            return JsonResponse({
                "code": LoginCode.NOT_LOGIN,
                "message": "用户未登录."
            })

        row: UserModel = UserModel.instance.get_user_by_uuid(uuid)
        if not row:
            return JsonResponse({
                "code": LoginCode.NOT_LOGIN,
                "message": "用户未登录."
            })
        else:
            request.session["uuid"] = row.uuid
            return self.get_response()

    @staticmethod
    def process_response(*args):
        return args[1]
