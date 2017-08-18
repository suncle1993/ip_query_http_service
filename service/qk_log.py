#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017/8/18 11:20
@author: Chen Liang
@function: log module
"""

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import os
import datetime
import logging
import logging.handlers

_console_logger = None
_warn_logger = None
_error_logger = None

CONSOLE_FILENAME = 'log/console.log'
WARNING_FILENAME = 'log/warn.log'
ERROR_FILENAME = 'log/error.log'


def log_init():
    if os.path.exists('log/') is True:
        pass
    else:
        os.mkdir('log/')
    global _console_logger, _warn_logger, _error_logger
    handler = logging.handlers.RotatingFileHandler(
        CONSOLE_FILENAME, maxBytes=20*1024*1024, backupCount=5)
    hdr = logging.StreamHandler()
    _console_logger = logging.getLogger('debug')
    _console_logger.addHandler(handler)
    _console_logger.addHandler(hdr)
    _console_logger.setLevel(logging.DEBUG)

    handler = logging.handlers.RotatingFileHandler(
        WARNING_FILENAME, maxBytes=20*1024*1024, backupCount=5)
    hdr = logging.StreamHandler()
    _warn_logger = logging.getLogger('warn')
    _warn_logger.addHandler(handler)
    _warn_logger.addHandler(hdr)
    _warn_logger.setLevel(logging.WARN)

    handler = logging.handlers.RotatingFileHandler(
        ERROR_FILENAME, maxBytes=20*1024*1024, backupCount=5)
    hdr = logging.StreamHandler()
    _error_logger = logging.getLogger('error')
    _error_logger.addHandler(handler)
    _error_logger.addHandler(hdr)
    _error_logger.setLevel(logging.ERROR)


def dlog(msg):
    file_name, file_no, unused = find_caller()
    time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    _console_logger.debug('[{}] [{}] [{},{}] {}'.format(time_str, 'debug', file_name, file_no, msg))


def ilog(msg):
    file_name, file_no, unused = find_caller()
    time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    _console_logger.info('[{}] [{}] [{},{}] {}'.format(time_str, 'info', file_name, file_no, msg))


def wlog(msg):
    file_name, file_no, unused = find_caller()
    time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    _console_logger.warn('[{}] [{}] [{},{}] {}'.format(time_str, 'warning', file_name, file_no, msg))
    _warn_logger.warn('[{}] [{}] [{},{}] {}'.format(time_str, 'warning', file_name, file_no, msg))


def elog(msg):
    file_name, file_no, unused = find_caller()
    time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    _console_logger.error('[{}] [{}] [{},{}] {}'.format(time_str, 'error', file_name, file_no, msg))
    _error_logger.error('[{}] [{}] [{},{}] {}'.format(time_str, 'error', file_name, file_no, msg))


def find_caller():
    f = sys._getframe(2)
    co = f.f_code
    return (os.path.basename(co.co_filename), f.f_lineno, co.co_name) if co is not None else ('unknown', 0, 'unknown')


if __name__ == '__main__':
    log_init()
    dlog('test.log {}'.format(123))
    ilog('test.log {}'.format(123))
    wlog('test.log {}'.format(123))
    elog('test.log {}'.format(123))
