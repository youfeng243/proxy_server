#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence
@file: view.py
@time: 2017/9/14 20:16
"""
import requests
from flask import Blueprint
from flask import request

from exts.common import log, success, fail, REMOTE_PROXY_CONF, LOCAL_HOST
from exts.database import redis

bp = Blueprint('proxy', __name__, url_prefix='/proxy')


# 获取动态代理服务
def get_dynamic_proxy(host):
    try:
        r = requests.get('http://{host}:{port}/proxy/{h}'.format(
            h=host, host=REMOTE_PROXY_CONF['host'], port=REMOTE_PROXY_CONF['port']),
            timeout=10)

        if r is None or r.status_code != 200 or 'failed' in r.text or 'False' in r.text:
            log.warn("动态代理服务异常, 重试...")
            return None

        proxies = 'http://{host}'.format(host=r.text)
        log.info('鲲鹏 ip = {}'.format(proxies))
        return proxies
    except Exception as e:
        log.error("动态代理访问异常:")
        log.exception(e)
    return None


# 获取代理功能
@bp.route('', methods=['POST'])
def get_proxy():
    if not request.is_json:
        log.warn("参数错误...")
        return fail()

    # {
    #     'username': 'beihai',
    #     'password': 'beihai',
    #     'type': 'static' or 'dynamic' // 这个参数保留，目前不一定用
    # }

    username = request.json.get('username')
    password = request.json.get('password')
    if not isinstance(username, basestring):
        log.error("用户错误，不是字符串: username = {} type = {}".format(username, type(username)))
        return fail('用户名类型错误!')

    if not isinstance(password, basestring):
        log.error("密码错误，不是字符串: password = {} type = {}".format(password, type(password)))
        return fail('密码类型错误!')

    # 判断当前用户是否在redis中
    origin_password = redis.get(username)
    if origin_password is None:
        log.error("当前用户不存在: username = {} password = {}".format(username, password))
        return fail('当前用户不存在!')

    if origin_password != password:
        log.error("密码错误: username = {} password = {}".format(username, password))
        return fail('密码错误!')

    # 请求动态代理服务
    proxy = get_dynamic_proxy(LOCAL_HOST)

    return success(proxy)
