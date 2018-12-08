#!/usr/bin/env python3
# -*- coding: utf-8  -*-

"""
XML-RPC 实现执行运行在远程机器上面的Python程序中的函数或方法的方式
由于 XML-RPC 将所有数据都序列化为XML格式，所以它会比其他的方式运行的慢一些。
这种方式的编码可以被绝大部分其他编程语言支持，其他语言的客户端程序都能访问你的服务。
实用 XML-RPC 可以快速构建一个简单远程过程调用系统。
仅仅是创建一个服务器实例， 通过它的方法 register_function() 来注册函数
然后使用方法 serve_forever() 启动它。 
"""

"""简单的键值存储服务器"""

from xmlrpc.server import SimpleXMLRPCServer

class KeyValueServer:
    _rpc_methods_ = ['get', 'set', 'delete', 'exists', 'keys']

    def __init__(self, address):
        self._data = {}
        self._serv = SimpleXMLRPCServer(address, allow_none=True)
        for name in self._rpc_methods_:
            self._serv.register_function(getattr(self, name))

    def get(self, name):
        return self._data.get(name)
    
    def set(self, name, value):
        self._data[name] = value
    
    def delete(self, name):
        del self._data[name]

    def exists(self, name):
        return name in self._data
    
    def keys(self):
        return list(self._data)
    
    def serve_forever(self):
        self._serv.serve_forever()
    
if __name__ == "__main__":
    kvserv = KeyValueServer(('', 15000))
    kvserv.serve_forever()

"""
客户端代码
from xmlrpc.client import ServerProxy
s = ServerProxy('http://lcoalhsot:15000', allow_none=True)
s.set('foo', bar)
s.set('spam', [1, 2, 3, 4])
s.keys()
s.get('foo')
s.get('spam')
s.delete('spam')
s.exists('spam')
"""

"""
XML-RPC暴露出来的函数只能适用于部分数据类型，比如字符串、整形、列表和字典。 
对于其他类型就得需要做些额外的功课了。 

"""