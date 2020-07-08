#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    feed
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    feed model

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from django.db import models

from reader.base.models._base import BaseModel


class FeedManager(models.Manager):
    pass


class FeedModel(BaseModel):
    class Meta:
        db_table = "reader_feed"

    objects = models.Manager()
    instance = FeedManager()

    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    feed_url = models.TextField()
    interval = models.PositiveIntegerField()
    status = models.PositiveSmallIntegerField()
    enabled = models.PositiveSmallIntegerField()
    author = models.PositiveIntegerField()
