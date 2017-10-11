# -*- coding: utf-8 -*-
from app import create_app
from exts.common import log
from werkzeug.contrib.fixers import ProxyFix

log.info("开始进入初始化流程..")
application = create_app('proxy_server')

application.wsgi_app = ProxyFix(application.wsgi_app)


@application.route("/home", methods=['GET'])
@application.route("/test", methods=['GET'])
@application.route("/index", methods=['GET'])
@application.route('/', methods=['GET'])
def index():
    log.info("proxy server is running...")
    return "proxy server is runing..."


if __name__ == "__main__":
    application.run(port=18585)
