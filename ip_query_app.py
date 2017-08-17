#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017/8/14 10:58
@author: Chen Liang
@function: provide ip_query http service
"""

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask
from service.qk_ipdb import IpTree
from service.error_handler import InvalidUsage
from flask import jsonify
from flask import request, make_response
import re


ip_app = Flask(__name__)


ip_tree = IpTree()
ip_tree.load_country_codes('service' + "/doc/country_list.txt")
ip_tree.load_china_province_codes('service' + "/doc/china_province_code.txt")
ip_tree.load_china_city_codes('service' + "/doc/china_city_code.txt")
ip_tree.loadfile('service' + "/doc/mydata4vipday2.dat")
pattern = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')


def is_ip(s):
    if pattern.match(s):
        return True
    else:
        return False


@ip_app.errorhandler(InvalidUsage)
def invalid_usage(error):
    response = make_response(error.message)
    response.status_code = error.status_code
    return response


@ip_app.route('/api/ip_query', methods=['POST'])
def ip_query():
    try:
        ip = request.json['ip']
    except KeyError as e:
        raise InvalidUsage('bad request: no key ip in your request json body. {}'.format(e), status_code=400)
    if not is_ip(ip):
        raise InvalidUsage('{} is not a ip'.format(ip), status_code=400)
    try:
        res = ip_tree.lookup(ip)
    except Exception as e:
        raise InvalidUsage('internal error: {}'.format(e), status_code=500)
    if res is not None:
        return jsonify(res)
    else:
        raise InvalidUsage('no ip info in ip db for ip: {}'.format(ip), status_code=501)


@ip_app.route('/api/ip_query', methods=['GET'])
def ip_query_get():
    try:
        ip = request.values.get('ip')
    except ValueError as e:
        raise InvalidUsage('bad request: no param ip in your request. {}'.format(e), status_code=400)
    if not is_ip(ip):
        raise InvalidUsage('{} is not a ip'.format(ip), status_code=400)
    try:
        res = ip_tree.lookup(ip)
    except Exception as e:
        raise InvalidUsage('internal error: {}'.format(e), status_code=500)
    if res is not None:
        return jsonify(res)
    else:
        raise InvalidUsage('no ip info in ip db for ip: {}'.format(ip), status_code=501)


if __name__ == '__main__':
    ip_app.debug = True
    ip_app.run()
