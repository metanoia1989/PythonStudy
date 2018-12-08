#!/usr/bin/env python3
# -*- coding: utf-8  -*-

"""
在不同的机器上面运行着多个Python解释器实例
希望能够在这些解释器之间通过消息来交换数据
使用 multiprocessing.connection 模块可以很容易的实现解释器之间的通信
PS: 感觉有点像消息列队服务器的意思，跨机器间通信
"""

"""简单的应答服务器"""

from multiprocessing.connection import Listener
import traceback

def echo_client(conn):
    try:
        while True:
            msg = conn.recv()
            conn.send(msg)
    except EOFError as e:
        print('连接已关闭')

def echo_server(address, authkey):
    serv = Listener(address, authkey=authkey)
    while True:
        try:
            client = serv.accept()
            echo_client(client)
        except Exception as e:
            traceback.print_exc()

if __name__ == "__main__":
    echo_server(('', 25000), authkey=b'peekaboo')

"""
客户端连接代码
跟底层socket不同的是，每个消息会完整保存（每一个通过send()发送的对象能通过recv()来完整接受）。
所有对象会通过pickle序列化。因此，任何兼容pickle的对象都能在此连接上面被发送和接受。

from multiprocessing.connection import Client
c = Client(('localhost', 25000), authkey=b'peekaboo')
c.send('hello')
c.recv()

c.send(42)
c.recv()

c.send([1, 2, 3, 4, 5])
c.recv()
"""

"""
有很多用来实现各种消息传输的包和函数库，比如ZeroMQ、Celery等
或者自己在底层socket基础之上来实现一个消息传输层
简单的方法是multiprocessing.connection，仅仅使用一些简单的语句即可实现多个解释器之间的消息通信。
解释器运行在同一台机器上面，可以使用另外的通信机制，比如Unix域套接字或者是Windows命名管道
s = Listener('/tmp/myconn', authkey=b'peekaboo')
s = Listener(r'\\.\pipe\myconn', authkey=b'peekaboo')
Client() 和 Listener() 中的 authkey 参数用来认证发起连接的终端用户。 如果密钥不对会产生一个异常。
multiprocessing.commection 模块最适合用来建立长连接（而不是大量的短连接）， 
例如，两个解释器之间启动后就开始建立连接并在处理某个问题过程中会一直保持连接状态。
需要对底层连接做更多的控制，比如需要支持超时、非阻塞I/O或其他类似的特性
使用另外的库或者是在高层socket上来实现这些特性。
"""