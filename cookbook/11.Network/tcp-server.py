#!/usr/bin/env python3
# -*- coding: utf-8  -*-

"""
现一个服务器，通过TCP协议和客户端通信
创建一个TCP服务器的一个简单方法是使用 socketserver 库
"""

from socketserver import BaseRequestHandler, StreamRequestHandler, TCPServer

class EchoHandler(BaseRequestHandler):
    """
    处理类，实现了 handle() 方法，用来为客户端连接服务
    :request 属性是客户端socket
    :client_address 有客户端地址
    """
    def handle(self):
        print('连接请求来自', self.client_address)
        while True:
            msg = self.request.recv(8192)
            if not msg:
                break
            self.request.send(msg)
    
class WriteHandler(StreamRequestHandler):
    def handle(self):
        print('连接请求来自', self.client_address)
        for line in self.rfile:
            self.wfile.write(line)
"""
if __name__ == "__main__":
    # serv = TCPServer(('', 20000), EchoHandler)
    serv = TCPServer(('', 20000), WriteHandler)
    serv.serve_forever()
"""    

"""
客户端连接代码
from socket import socket,  AF_INET, SOCK_STREAM
s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 20000))
s.send(b'Hello')
s.recv(8192)
"""


"""
socketserver 可以让我们很容易的创建简单的TCP服务器。 
但是，你需要注意的是，默认情况下这种服务器是单线程的，一次只能为一个客户端连接服务。 
如果你想处理多个客户端，可以初始化一个 ForkingTCPServer 或者是 ThreadingTCPServer 对象。
"""

if __name__ == "__main__":
    from threading import Thread
    NWORKERS = 16
    serv = TCPServer(('', 20000), EchoHandler)
    for n in range(NWORKERS):
        t = Thread(target=serv.serve_forever)
        t.daemon = True
        t.start()
    serv.serve_forever()


"""
一个 TCPServer 在实例化的时候会绑定并激活相应的 socket
调整底下的 socket ，可以设置参数 bind_and_activate=False
"""
if __name__ == "__main__":
    serv = TCPServer(('', 20000), EchoHandler, bind_and_activate=False)
    serv.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    serv.server_bind()
    serv.server_activate()
    serv.serve_forever()