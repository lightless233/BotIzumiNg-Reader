#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    user
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    用户模型

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import datetime
import uuid

from django.db import models

from reader.base.models._base import BaseModel


class UserManager(models.Manager):
    def get_user_by_email(self, email):
        return self.filter(is_deleted=0, email=email).first()

    def get_user_by_nickname(self, nickname):
        return self.filter(is_deleted=0, nickname=nickname).first()

    def get_user_by_uuid(self, _uuid):
        return self.filter(is_deleted=0, uuid=_uuid).first()

    def add_user(self, nickname, email, password):
        u = uuid.uuid1()
        return self.create(nickname=nickname, email=email, password=password, uuid=u)


class UserModel(BaseModel):
    class Meta:
        db_table = "reader_user"

    objects = models.Manager()
    instance = UserManager()

    uuid = models.CharField(max_length=128)
    nickname = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    password = models.CharField(max_length=512)

    # 账号状态，
    # 0-未激活，1-正常，2-被封禁
    status = models.PositiveSmallIntegerField(default=0)

    # 最后一次登录时间
    last_login_time = models.DateTimeField(default=datetime.datetime.now)

    # 最后一次登录 IP
    last_login_ip = models.CharField(max_length=16, default="255.255.255.255")
