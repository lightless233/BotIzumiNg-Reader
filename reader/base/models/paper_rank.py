#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    paper_rank.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    PaperRank model

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from django.db import models

from reader.base.models._base import BaseModel


class PaperRankManager(models.Manager):
    pass


class PaperRankModel(BaseModel):
    class Meta:
        db_table = "reader_paper_rank"

    objects = models.Manager()
    instance = PaperRankManager()

    paper_id = models.BigIntegerField()
    rank = models.PositiveSmallIntegerField()
    author = models.PositiveIntegerField()
