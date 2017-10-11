#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence
@file: view.py
@time: 2017/9/14 20:16
"""

from flask import Blueprint
from flask import request

from exts.common import log, success, fail

bp = Blueprint('proxy', __name__, url_prefix='/proxy')


# 获取代理功能
@bp.route('', methods=['POST'])
def get_proxy():
    if not request.is_json:
        log.warn("参数错误...")
        return fail()

    return success()
