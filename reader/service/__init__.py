#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    __init__.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""


class BaseService:

    def _build_result(self, check_result, obj=None):
        # 这里其实应该用 namedTuple，为了简单先这么写，下次再改
        return {"check_result": check_result, "obj": obj}
