#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    start
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    程序启动入口

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from django.core.management import BaseCommand

from reader import g
from reader.application import Application


class Command(BaseCommand):
    help = "Start bot izumi-ng reader."

    def handle(self, *args, **options):

        self.stdout.write(self.style.SUCCESS("Starting izumi-ng reader."))

        try:
            g.application = app = Application()
            app.start()
        except Exception as e:
            self.stdout.write(f"Error while starting izumi-ng reader, error: {e}")

            import sys, traceback
            full_err = ''.join(traceback.TracebackException(*sys.exc_info()).format())
            self.stdout.write(f"Full error below:\n {full_err}")
