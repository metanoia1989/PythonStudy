#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import time 

_hello_resp = '''\
<html>
  <head>
     <title>Hello {name}</title>
   </head>
   <body>
     <h1>Hello {name}!</h1>
   </body>
</html>'''

def hello_world(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    params = environ.get('params')
    resp = _hello_resp.format(name=params.get('name'))
    yield resp.encode('utf-8')

_localtime_resp = '''\
<?xml version="1.0"?>
<time>
    <year>{t.tm_year}</year>
    <month>{t.tm_mon}</month>
    <day>{t.tm_mday}</day>
    <hour>{t.tm_hour}</hour>
    <minute>{t.tm_min}</minute>
    <second>{t.tm_sec}</second>
</time>
'''

def localtime(environ, start_response):
    start_response('200 OK', [('Content-type', 'application/xml')])
    resp = _localtime_resp.format(t=time.localtime())
    yield resp.encode('utf-8')

if __name__ == "__main__":
    from resty import PathDispatcher
    from wsgiref.simple_server import make_server

    # 创建调度器和注册函数
    dispatcher = PathDispatcher()
    dispatcher.register('GET', '/hello', hello_world)
    dispatcher.register('GET', '/localtime', localtime)

    # 运行基本服务
    httpd = make_server('', 8080, dispatcher)
    print('服务运行于端口 8080....')
    httpd.serve_forever()

