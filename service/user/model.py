#!/usr/bin/env python
# encoding: utf-8
"""
@author: youfeng
@email: youfeng243@163.com
@license: Apache Licence
@file: user.py
@time: 2017/8/29 17:58
"""
from sqlalchemy.exc import IntegrityError

from exts.common import log
from exts.database import db
from exts.model_base import ModelBase


class User(ModelBase):
    __tablename__ = 'user'

    # 用户名
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)

    # 密码
    password = db.Column(db.String(256), nullable=False)

    @classmethod
    def create(cls, username, password):
        user = cls(
            username=username, password=password)

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            log.error("主键重复: username = {} password = {}".format(
                username, password))
            db.session.rollback()
            return None, False
        except Exception as e:
            log.error("未知插入错误: username = {} password = {}".format(
                username, password))
            log.exception(e)
            return None, False
        return user, True

    def __repr__(self):
        return '<User {}>'.format(self.mobile)

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
