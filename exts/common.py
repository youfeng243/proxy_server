#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence
@file: common.py
@time: 2017/8/28 20:58
"""

import json

from flask import Response

from logger import Logger

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_SERVER_ERROR = 500
HTTP_NOT_IMPLEMENTED = 501

ERROR_MSG = {
    HTTP_OK: 'OK',
    HTTP_BAD_REQUEST: 'bad request',
    HTTP_UNAUTHORIZED: 'unauthorized',
    HTTP_FORBIDDEN: 'forbidden',
    HTTP_NOT_FOUND: 'not found',
    HTTP_SERVER_ERROR: 'server error',
    HTTP_NOT_IMPLEMENTED: 'not implemented',
}

# 代理服务
REMOTE_PROXY_CONF = {
    'host': '112.74.163.187',
    'port': 9300,
}

LOCAL_HOST = '101.132.128.78'

log = Logger('proxy_server.log').get_logger()


def json_resp(data, http_status):
    return Response(data, status=http_status, mimetype="application/json")


def fail(msg='error'):
    resp = {
        'success': False,
        'proxy': None,
        'type': None,
        'error': msg,
    }

    data = json.dumps(resp)
    return json_resp(data, HTTP_OK)


# 返回成功
def success(proxy=None):
    resp = {
        'success': True,
        'proxy': None,
        'type': None
    }

    if proxy is None or proxy == '':
        resp['success'] = False
        data = json.dumps(resp)
        return json_resp(data, HTTP_OK)

    if 'http' in proxy:
        resp['type'] = 'http'
    elif 'socks5' in proxy:
        resp['type'] = 'socks5'

    resp['proxy'] = proxy
    data = json.dumps(resp)
    return json_resp(data, HTTP_OK)

# def encode_username(username):
#     '''
#     This will encode a ``unicode`` value into a cookie, and sign that cookie
#     with the app's secret key.
#
#     :param username: The value to encode, as `unicode`.
#     :type username: unicode
#     '''
#     return u'{0}|{1}'.format(str(username), _cookie_digest(str(username)))
#
#
# def decode_username(cookie):
#     '''
#     This decodes a cookie given by `encode_cookie`. If verification of the
#     cookie fails, ``None`` will be implicitly returned.
#
#     :param cookie: An encoded cookie.
#     :type cookie: str
#     '''
#     try:
#         payload, digest = cookie.rsplit(u'|', 1)
#         if hasattr(digest, 'decode'):
#             digest = digest.decode('ascii')  # pragma: no cover
#     except ValueError:
#         return None
#
#     if safe_str_cmp(_cookie_digest(payload), digest):
#         return payload
#
#     return None
