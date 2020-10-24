#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    _base
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import abc
from typing import Dict, Optional

from django.views import View


class BaseView(View, metaclass=abc.ABCMeta):

    def __init__(self):
        super(BaseView, self).__init__()

        self.current_user: Optional[Dict] = None

    def check_login(self, request) -> bool:
        current_user = request.session.get("user")
        if not current_user:
            return False
        else:
            self.current_user = current_user
            return True
