#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    user.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    用户相关的接口

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import jwt
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.views import View
from django.conf import settings

from reader.api.controller import json_response
from reader.base.constant import ResponseCode
from reader.base.models import UserModel
from reader.util.logger import logger
from reader.util.validator import RequestValidator


class RegisterView(View):

    @json_response
    def post(self, request):

        validate_result = RequestValidator.check(request, {
            "nickname": {"empty": True},
            "email": {"empty": True},
            "password": {"empty": True},
        }, RequestValidator.Methods.POST_JSON)

        if validate_result.error:
            msg = validate_result.error_message
            logger.error(f"error: {msg}")
            return {"code": 4001, "message": msg}

        params_map = validate_result.params

        # 检查这个用户有没有注册过
        if not self.__check(params_map.get("email"), params_map.get("nickname")):
            return {
                "code": ResponseCode.ERROR_PARAMS,
                "message": "[nickname] or [email] already exist."
            }

        # 存 db
        real_password = make_password(params_map.get("password"), settings.PASSWORD_SALT)
        user = UserModel.instance.add_user(
            params_map.get("nickname"),
            params_map.get("email"),
            real_password
        )

        if user:
            return {
                "code": ResponseCode.SUCCESS,
                "message": "Register success!"
            }
        else:
            return {
                "code": ResponseCode.ERROR_DB,
                "message": "Register error."
            }

    @staticmethod
    def __check(email: str, nickname: str) -> bool:
        r1 = UserModel.instance.get_user_by_email(email)
        r2 = UserModel.instance.get_user_by_nickname(nickname)
        if r1 or r2:
            return False
        else:
            return True


class LoginView(View):

    @staticmethod
    def post(request):
        validate_result = RequestValidator.check(request, {
            "email": {"empty": True},
            "password": {"empty": True},
        }, RequestValidator.Methods.POST_JSON)

        if validate_result.error:
            msg = validate_result.error_message
            logger.error(f"error: {msg}")
            return JsonResponse({"code": 4001, "message": msg})

        params_map = validate_result.params

        user: UserModel = UserModel.instance.get_user_by_email(params_map.get("email"))
        if not user:
            return JsonResponse({
                "code": ResponseCode.ERROR_RUNTIME,
                "message": "[email] or [password] error."
            })

        # 检查密码是否正确
        if not check_password(params_map.get("password"), user.password):
            return JsonResponse({
                "code": ResponseCode.ERROR_RUNTIME,
                "message": "[email] or [password] error."
            })

        # 生成 JWT
        # {
        #   "uuid": member-uuid,
        # }
        # TODO: web 应用启动的时候，需要判断是否有配置 JWT_TOKEN PASSWORD_SALT
        token = jwt.encode({"id": user.uuid}, settings.JWT_SECRET)
        response = JsonResponse({
            "code": ResponseCode.SUCCESS,
            "message": "Login success!"
        })
        response.set_cookie("X-READER-AUTH", token.decode("UTF-8"), samesite="Lax")
        return response
