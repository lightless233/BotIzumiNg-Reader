#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    group_feed.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    群组中订阅了哪些 feeds

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from django.db import models

from reader.base.models._base import BaseModel


class GroupFeedsManager(models.Manager):
    pass


class GroupFeedsModel(BaseModel):
    class Meta:
        db_table = "reader_group_feeds"

    objects = models.Manager()
    instance = GroupFeedsManager()

    group_id = models.BigIntegerField(default=0)
    feeds_id = models.BigIntegerField(default=0)
