#!/usr/bin/env python3
# -*- coding: utf-8  -*-

"""
通过HTTP协议以客户端的方式访问多种服务，下载数据或者与基于REST的API进行交互。
"""

from urllib import request, parse
import requests

print('\n', '*'*5, '使用 urllib 标准库', '*'*5)

url = 'http://httpbin.org/get'
params = {
    'name1': 'value1',
    'name2': 'value2',
}
querystring = parse.urlencode(params)

"""get 请求"""
u = request.urlopen(url + '?' + querystring)
resp = u.read()
print('#' * 5, 'get请求', '#' * 5)
print(resp)
print('#' * 5, 'get请求', '#' * 5)

"""post 请求""" 
url = 'http://httpbin.org/post'
u = request.urlopen(url, querystring.encode('ascii'))
resp = u.read()
print('#' * 5, 'post请求', '#' * 5)
print(resp)
print('#' * 5, 'post请求', '#' * 5)

"""
自定义 HTTP 头
如修改 user-agent 字段,可以创建一个包含字段值的字典，
并创建一个Request实例然后将其传给 urlopen() 
"""
headers = {
    'User-Agent': 'none/ofyoubusiness',
    'Spam': 'Eggs'
}
req = request.Request(url, querystring.encode('ascii'), headers=headers)
u = request.urlopen(req)
resp = u.read()
print('#' * 5, '自定义HTTP头', '#' * 5)
print(resp)
print('#' * 5, '自定义HTTP头', '#' * 5)

"""
使用 requests 库 发起http请求
"""
print('\n', '*'*5, '使用 requests 库', '*'*5)
resp = requests.post(url, data=params, headers=headers)
print('unicode编码响应文本 {}'.format(resp.text))
print('原始二进制数据 {}'.format(resp.content))
print('json格式响应数据 {}'.format(resp.json))

# 发起 HEAD 请求
resp = requests.head('https://www.python.org')
status = resp.status_code
last_modified = resp.headers.get('last-modified')
content_type = resp.headers.get('content-type')
content_length = resp.headers.get('content-length')
print('status code: {}, last_modified: {}, content_type: {}, content_length: {}'\
        .format(status, last_modified, content_type, content_length))

# 基本认证登陆
# resp = requests.get('https://pypi.python.org/pypi?:action=login', 
#                     auth=('user', 'password'))

# 传递 cookies
# resp1 = request.get(url)
# resp2 = request.get(url, cookies=resp1.cookies)

# 上传文件
files = { 'file': ('data.csv', open('data.csv', 'rb')) }
resp = requests.post(url, files=files)
print('文件上传响应 {}'.format(resp.text))


"""
坚持使用标准的程序库发送各种http请求，需要使用底层的 http.client 模块来实现自己的代码
编写涉及代理、认证、cookies以及其他一些细节方面的代码会非常繁琐
在开发过程中测试HTTP客户端代码如cookies、认证、HTTP头、编码方式等，使用httpbin服务。
这个站点会接收发出的请求，然后以JSON的形式将相应信息回传回来。
"""

