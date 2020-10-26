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
import time

import jwt
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from reader.base.constant import AUTH_TOKEN, NOT_LOGIN_JSON
from reader.base.models import UserModel
from reader.util.logger import logger


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

        h_auth_token = request.META.get("HTTP_" + AUTH_TOKEN.replace("-", "_").upper())
        if h_auth_token is None:
            return JsonResponse(NOT_LOGIN_JSON)

        try:
            # {"id": "uuid"}
            result: dict = jwt.decode(h_auth_token, settings.JWT_SECRET)
            uuid = result.get("id")
            expire = result.get("expire")
        except jwt.exceptions.PyJWTError as e:
            logger.error(f"Error when decode jwt, value: {h_auth_token}, error: {e}")
            return JsonResponse(NOT_LOGIN_JSON)

        if uuid is None or expire is None:
            return JsonResponse(NOT_LOGIN_JSON)

        # 检查 token 是否过期了
        current_time = int(time.time())
        if current_time > int(expire):
            return JsonResponse(NOT_LOGIN_JSON)

        row: UserModel = UserModel.instance.get_user_by_uuid(uuid)
        if not row:
            return JsonResponse(NOT_LOGIN_JSON)
        else:
            # 用户处于登录态，在 session 里写一份用户信息
            # 同时把 token 挂到 response 上
            user_dict = {
                "uuid": row.uuid,
                "id": row.id,
                "nickname": row.nickname,
                "email": row.email,
            }
            request.session["user"] = user_dict
            return self.get_response(request)

    def process_response(self, request, response):

        # 只有 /api/ 下面的接口才校验是否登录
        if not request.path.startswith("/api/"):
            return self.get_response(request)

        h_auth_token = request.META.get("HTTP_" + AUTH_TOKEN.replace("-", "_").upper())
        if h_auth_token is None:
            return JsonResponse(NOT_LOGIN_JSON)

        # 解开 JWT
        try:
            result: dict = jwt.decode(h_auth_token, settings.JWT_SECRET)
        except jwt.exceptions.PyJWTError as e:
            logger.error(f"Error when decode jwt, value: {h_auth_token}, error: {e}")
            return JsonResponse(NOT_LOGIN_JSON)

        uuid = result.get("id")
        expire_time = result.get("expire")

        if uuid is None or expire_time is None:
            return JsonResponse(NOT_LOGIN_JSON)

        row: UserModel = UserModel.instance.get_user_by_uuid(uuid)
        if not row:
            return JsonResponse(NOT_LOGIN_JSON)
        else:
            # uuid 有对应的用户，更新出新的token
            new_token = jwt.encode({"id": uuid, "expire": int(expire_time) + 3600 * 24}, settings.JWT_SECRET)
            response[AUTH_TOKEN] = new_token.decode("UTF-8")

        return response
