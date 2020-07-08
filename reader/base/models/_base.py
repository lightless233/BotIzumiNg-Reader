#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    _base.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    base model

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
