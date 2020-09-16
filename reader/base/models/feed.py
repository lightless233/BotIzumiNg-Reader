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
import datetime

from django.db import models
from django.db import transaction

from reader.base.models._base import BaseModel


class FeedManager(models.Manager):

    def all(self):
        return self.filter(is_deleted=0).all()

    def get_feed_by_id(self, feed_id):
        return self.filter(is_deleted=0, id=feed_id).first()

    def update_feed_by_id(self, feed_id, **kwargs):
        return self.filter(is_deleted=0, id=feed_id).update(
            name=kwargs.get("name"),
            description=kwargs.get("description"),
            feed_url=kwargs.get("feed_url"),
            interval=kwargs.get("interval"),
            enabled=kwargs.get("enabled"),
        )

    def delete_feed_by_id(self, feed_id):
        return self.filter(is_deleted=0, id=feed_id).update(is_deleted=1)

    def switch_feed_enabled_by_id(self, feed_id):
        with transaction.atomic():
            obj = self.filter(is_deleted=0, id=feed_id).first()
            obj.enabled = not obj.enabled
            obj.save()

            return obj


class FeedModel(BaseModel):
    class Meta:
        db_table = "reader_feed"

    objects = models.Manager()
    instance = FeedManager()

    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    feed_url = models.TextField()
    interval = models.PositiveIntegerField()

    # 该源的当前状态
    # 0-待更新，1-更新中，2-存活，3-已死亡
    status = models.PositiveSmallIntegerField()

    # 是否开启
    # 0-关闭，1-开启
    enabled = models.PositiveSmallIntegerField()

    # 订阅源的健康状态
    # 0-默认状态，1-活跃更新，2-不活跃更新，3-无法连通
    health_status = models.PositiveSmallIntegerField(default=0)

    last_refresh_time = models.DateTimeField(default=datetime.datetime.now)
    author = models.PositiveIntegerField()

    def convert(self):
        return {
            "feedName": self.name,
            "description": self.description,
            "feedUrl": self.feed_url,
            "interval": int(self.interval),
            "status": int(self.status),
            "enabled": int(self.enabled),
            "healthStatus": int(self.health_status),
            "lastRefreshTime": self.last_refresh_time,
            "author": self.author,
        }
