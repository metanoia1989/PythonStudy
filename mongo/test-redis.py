#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import redis

# client = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)
redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True, db=0)
rcli = redis.StrictRedis(connection_pool=redis_pool)

rcli.set('name', 'hello world')