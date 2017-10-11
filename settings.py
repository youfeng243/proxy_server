#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence
@file: settings.py
@time: 2017/9/4 20:30
"""
DEBUG = False

SECRET_KEY = "4&^^%%$%BJHGFGHHVVBN%$$#^"
SQLALCHEMY_DATABASE_URI = 'mysql://root:000000@localhost:3306/proxy_server_db?charset=utf8'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
REDIS_URI = "redis://localhost:6379"
# redis 最大连接数
REDIS_MAX_CONNECTIONS = 32
