#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
网络框架系统中的请求对象等等类
"""

class Request(object):
    """
    请求对象
    """
    def __init__(self, headers, url, body, GET, POST):
        self.headers = headers
        self.url = url
        self.body = body
        self.GET = GET
        self.POST = POST

    
class Response(object):
    """
    响应对象
    """
    def __init__(self, headers, status_code, body):
        self.headers = headers
        self.status_code = status_code
        self.body = body

class User(object):
    """
    User模型类
    """
    pass

def get_user_object(username, password):
    return User.find_by_token(username, password)
