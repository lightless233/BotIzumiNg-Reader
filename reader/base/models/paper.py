#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    paper
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    paper model

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import datetime

from django.db import models

from reader.base.models._base import BaseModel


class PaperManager(models.Manager):
    pass


class PaperModel(BaseModel):
    class Meta:
        db_table = "reader_paper"

    objects = models.Manager()
    instance = PaperManager()

    feed_id = models.BigIntegerField()
    title = models.CharField(max_length=512)
    content = models.TextField()
    link = models.TextField(default="")
    unique_hash = models.CharField(max_length=64)
    tags = models.TextField()
    pushed_status = models.PositiveSmallIntegerField()
    pushed_time = models.DateTimeField(default=datetime.datetime.now)
    rank = models.PositiveSmallIntegerField(default=0)

    # paper的发布时间，这个时间是取的原始时间，没有处理过
    publish_time = models.TextField()
