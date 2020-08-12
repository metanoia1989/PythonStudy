#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint

# pprint模块可以打印像词典和列表这样的数据类型，以格式化的方式。
pp = pprint.PrettyPrinter(indent=4)

"""
启动方法 uwsgi --http :9090 --wsgi-file hello_world_server.py
"""
def application(env, start_response):
    pp.pprint(env)

    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b"Hello World"]