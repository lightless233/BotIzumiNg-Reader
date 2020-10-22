#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    group_info
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    GROUP 相关的模型

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from django.db import models

from reader.base.models._base import BaseModel


class GroupInfoManager(models.Manager):
    pass


class GroupInfoModel(BaseModel):
    class Meta:
        db_table = "reader_group_info"

    objects = models.Manager()
    instance = GroupInfoManager()

    uuid = models.CharField(max_length=128)
    group_name = models.CharField(max_length=128)
    owner = models.BigIntegerField(default=0)
    description = models.CharField(max_length=512)

    # 是否为私有群组，0-公开群组，1-私有群组
    private = models.SmallIntegerField(default=0)

    # TODO 需要更多信息，比如邀请入群的部分，加群码之类的
