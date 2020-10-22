#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    group_member.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    记录群组中的用户信息

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from django.db import models

from reader.base.models._base import BaseModel


class GroupMemberManager(models.Manager):
    pass


class GroupMemberModel(BaseModel):
    class Meta:
        db_table = "reader_group_member"

    objects = models.Manager()
    instance = GroupMemberManager()

    group_id = models.BigIntegerField(default=0)
    member_id = models.BigIntegerField(default=0)

    # 成员在群组中的状态
    # 0-正常，1-被封禁，2-未激活，3-未审批
    status = models.SmallIntegerField(default=0)
