# -*- coding:utf8 -*-


import redis

import config

redis_db = redis.Redis(connection_pool=redis.ConnectionPool(**config.redis))
