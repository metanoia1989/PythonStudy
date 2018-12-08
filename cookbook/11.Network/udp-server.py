#!/usr/bin/env python3
# -*- coding: utf-8  -*-

"""
实现一个基于UDP协议的服务器来与客户端通信
通过使用 socketserver 库创建
"""

from socketserver import BaseRequestHandler, UDPServer
import time

class TimeHandler(BaseRequestHandler):
    def handle(self):
        print('连接请求来自', self.client_address)
        msg, sock = self.request
        resp = time.ctime()
        sock.sendto(resp.encode('ascii'), self.client_address)
    
if __name__ == "__main__":
    serv = UDPServer(('', 20000), TimeHandler)
    serv.serve_forever()

"""
udp 客户端
from socket import socket, AF_INET, SOCK_DGRAM
s = socket(AF_INET, SOCK_DGRAM)
s.sendto(b'',   ('localhost', 20000))
s.recvfrom(8192)
"""


"""
UDP服务器接收到达的数据报(消息)和客户端地址
如果服务器需要做应答， 它要给客户端回发一个数据报。
对于数据报的传送，使用socket的 sendto() 和 recvfrom() 方法。
传统的 send() 和 recv() 也可以，但一般用于 tcp
"""

"""
UDP天生是不可靠的（因为通信没有建立连接，消息可能丢失）
需要自行处理丢失消息的情况
如果可靠性对于你程序很重要，你需要借助于序列号、重试、超时以及一些其他方法来保证。
UDP通常被用在那些对于可靠传输要求不是很高的场合。
例如，在实时应用如多媒体流以及游戏领域， 无需返回恢复丢失的数据包（程序只需简单的忽略它并继续向前运行）。
"""

"""
UDPServer 类是单线程的，也就是说一次只能为一个客户端连接服务
并发操作，可以实例化一个 ForkingUDPServer 或 ThreadingUDPServer 对象
"""
from socketserver import ThreadingUDPServer
if __name__ == "__main__":
    serv = ThreadingUDPServer(('', 20000), TimeHandler)
    serv.serve_forever()

"""
直接使用 socket 来实现一个UDP服务器也不难
"""
from socket import socket, AF_INET, SOCK_DGRAM
import time

def time_server(address):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(address)
    while True:
        msg, addr = sock.recvfrom(8192)
        print('连接请求来自', addr)
        resp = time.ctime()
        sock.sendto(resp.encode('ascii'), addr)

if __name__ == '__main__':
    time_server(('', 20000))