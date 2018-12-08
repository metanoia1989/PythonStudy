#!/usr/bin/env python3
# -*- coding: utf-8  -*-

"""
使用一个简单的REST接口通过网络远程控制或访问你的应用程序
构建一个REST风格的接口最简单的方法是创建一个基于WSGI标准（PEP 3333）的很小的库
"""


import cgi

def notfound_404(environ, start_response):
    start_response('404 Not Found', [ ('Content-type', 'text/plain') ])
    return [b'Not Found']

class PathDispatcher:
    def __init__(self):
        self.pathmap = { }
    
    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO')
        params = cig.FieldStorage(environ.get['wsgi.input'], environ=environ)

        method = environ.get('REQUEST_METHOD').lower()
        environ['params'] = { key: params.getvalue(key) for key in params }
        handler = self.pathmap.get((method, path), notfound_404)
        return handler(environ, start_response)
    
    def register(self, method, path, function):
        self.pathmap[method.lower, path] = function
        return function


"""
在编写REST接口时，通常都是服务于普通的HTTP请求。
跟功能完整的网站相比，REST接口只需要处理数据。 
这些数据以各种标准格式编码，比如XML、JSON或CSV.
长期运行的程序可能会使用一个REST API来实现监控或诊断。 
大数据应用程序可以使用REST来构建一个数据查询或提取系统。
REST还能用来控制硬件设备比如机器人、传感器、工厂或灯泡。
REST API已经被大量客户端编程环境所支持，比如Javascript, Android, iOS等。 
因此，利用这种接口可以让你开发出更加复杂的应用程序。
"""

"""
WSGI本身是一个很小的标准。因此它并没有提供一些高级的特性比如认证、cookies、重定向等。 
这些你自己实现起来也不难。不过如果你想要更多的支持，可以考虑第三方库，比如 WebOb 或者 Paste
"""