# -*- coding: utf-8 -*-

from __future__ import absolute_import

import redis as r_

import settings
from exts.common import log


class Redis(object):
    def __init__(self):
        self._client = r_.StrictRedis.from_url(settings.REDIS_URI, max_connections=settings.REDIS_MAX_CONNECTIONS)
        log.info("redis 初始化完成!!")

    def __getattr__(self, name):
        return getattr(self._client, name)
