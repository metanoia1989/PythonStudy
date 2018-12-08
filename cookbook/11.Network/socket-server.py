#!/usr/bin/env python3
# -*- coding: utf-8  -*-

"""
Python的高层网络模块（比如HTTP、XML-RPC等）都是建立在 socketserver 功能之上
"""

from socket import socket, AF_INET, SOCK_STREAM

def echo_handler(address, client_sock):
    print('连接请求来自', address)
    while True:
        msg = client_sock.recv(8192)
        if not msg:
            break
        client_sock.sendall(msg)
    client_sock.close()

def echo_server(address, backlog=5):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(backlog)
    while True:
        client_sock, client_addr = sock.accept()
        echo_handler(client_addr, client_sock)
    
if __name__ == "__main__":
    echo_server(('', 20000))