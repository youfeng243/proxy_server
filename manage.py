# -*- coding: utf-8 -*-

from __future__ import absolute_import

from app import create_app
from exts.database import db
from flask_script import Manager
from setuptools import find_packages

from service.user.model import User

application = create_app('proxy_server')
manager = Manager(application)

USERNAME = "beihai"
PASSWORD = "beihai"


def _import_models():
    puff_packages = find_packages('./service')
    for each in puff_packages:
        guess_module_name = 'service.%s.model' % each
        try:
            __import__(guess_module_name, globals(), locals())
            print 'Find model:', guess_module_name
        except ImportError:
            pass


@manager.command
def syncdb():
    # with application.test_request_context():
    _import_models()

    db.create_all()
    db.session.commit()

    if User.get_by_username(USERNAME) is None:
        User.create(USERNAME, PASSWORD)

        print '数据库创建完成...'


@manager.command
def dropdb():
    with application.test_request_context():
        _import_models()
        db.drop_all()
        db.session.commit()
        print '数据库删除完成...'


if __name__ == '__main__':
    manager.run()
