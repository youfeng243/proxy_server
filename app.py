# !/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence
@file: gun.config.py
@time: 2017/8/28 20:45
"""
import json

from flask import Flask
from flask import request

import settings
from exts.common import log, fail
from exts.database import db, redis
from service.user.model import User
from service.user.view import bp as user_bp


def create_app(name=None):
    app = Flask(name or __name__)

    # 从settings中加载配置信息
    app.config.from_object('settings')

    app.debug = settings.DEBUG

    # 数据库初始化
    db.init_app(app)

    # 初始化redis数据
    app.before_first_request(init_user_info)

    # 设置错误处理流程
    setup_error_handler(app)

    # 注册蓝图
    register_bp(app)

    # 注册访问日志钩子
    setup_hooks(app)

    log.info("flask 服务初始化完成...")
    return app


# 初始化用户信息
def init_user_info():
    user_list = User.get_all()

    for user in user_list:
        # todo 目前账户不过期，后续改为默认一天后过期
        # redis.setex(user.username, 24 * 3600, user.password)
        redis.set(user.username, user.password)
        log.info("加载当前用户到redis: username = {} password = {}".format(user.username, user.password))

    log.info("加载用户数据完成...")


# 注册蓝图
def register_bp(app):
    app.register_blueprint(user_bp)


def _get_remote_addr():
    address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if address is not None:
        # An 'X-Forwarded-For' header includes a comma separated list of the
        # addresses, the first address being the actual remote address.
        address = address.encode('utf-8').split(b',')[0].strip()
    return address


def _request_log(resp, *args, **kwargs):
    log.info(
        '{addr} request: [{status}] {method}, '
        'url: {url}'.format(addr=_get_remote_addr(),
                            status=resp.status,
                            method=request.method,
                            url=request.url,
                            )
    )
    # 不是debug模式下也需要打印数据信息
    if resp.mimetype == 'application/json':
        data = resp.get_data()
        log.info("response: {}".format(json.dumps(json.loads(data), ensure_ascii=False)))
    return resp


def setup_hooks(app):
    app.after_request(_request_log)


def setup_error_handler(app):
    @app.errorhandler(400)
    @app.errorhandler(ValueError)
    def http_bad_request(e):
        log.exception(e)
        return fail()

    @app.errorhandler(403)
    def http_forbidden(e):
        log.exception(e)
        return fail()

    @app.errorhandler(404)
    def http_not_found(e):
        log.exception(e)
        return fail()

    @app.errorhandler(500)
    @app.errorhandler(Exception)
    def http_server_error(e):
        log.exception(e)
        return fail()
