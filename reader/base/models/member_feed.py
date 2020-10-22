#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    member_feed.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    用户订阅的 feed 信息
    哪个用户订阅了哪个 feed

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from django.db import models

from reader.base.models._base import BaseModel


class MemberFeedsManager(models.Manager):
    pass


class MemberFeedsModel(BaseModel):
    class Meta:
        db_table = "reader_member_feeds"

    objects = models.Manager()
    instance = MemberFeedsManager()

    member_id = models.BigIntegerField(default=0)
    feeds_id = models.BigIntegerField(default=0)
