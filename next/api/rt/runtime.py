#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import sys

class RtInit:

    cwd: str
    cwd = os.path.dirname(__file__)

    started: bool
    started = False

    def __init__(self, *args, **kwargs):

        self.__dict__.update(**kwargs)

        self.rinit()

    def rinit(self):

        if not self.started:
            if self.cwd not in sys.path:

                sys.path.insert(0, self.cwd)
                self.started = True