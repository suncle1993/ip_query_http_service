#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017/8/14 16:01
@author: Chen Liang
@function: customized exception class: InvalidUsage
"""

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=400):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

