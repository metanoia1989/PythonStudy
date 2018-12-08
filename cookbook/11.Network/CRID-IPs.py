#!/usr/bin/env python3
# -*- coding: utf-8  -*-

"""
一个CIDR网络地址比如“123.45.67.89/27” 将其转换成它所代表的所有IP 
比如，“123.45.67.64”, “123.45.67.65”, …, “123.45.67.95”)
使用 ipaddress 模块完成计算
ipaddress 模块有很多类可以表示IP地址、网络和接口, 操作网络地址（比如解析、打印、验证等）非常实用
"""

import ipaddress

print('****ipv4地址****')
net = ipaddress.ip_network('123.45.67.64/27')
for a in net:
    print('ip地址：', a)
print('***************\n')

print('****ipv6地址****')
net6 = ipaddress.ip_network('12:3456:78:90ab:cd:ef01:23:30/125')
for a in net6:
    print('ip地址：', a)
print('***************\n')

"""Network 也允许像数组一样的索引取值"""
print(net6.num_addresses)
print(net[0])
print(net[1])
print(net[-1])
print(net[-2])

"""执行网络成员检查的操作"""
a_ip = ipaddress.ip_address('123.45.67.69')
b_ip = ipaddress.ip_address('123.45.67.123')
print(a_ip in net)
print(b_ip in net)

"""通过ip接口来创建CIDR网络地址"""
inet = ipaddress.ip_interface('123.45.67.73/27')
print(inet.network)
print(inet.ip)

"""
fipaddress 模块跟其他一些和网络相关的模块比如 socket 库交集很少
不能使用 IPv4Address 的实例来代替一个地址字符串，你首先得显式的使用 str() 转换它。
"""
a = ipaddress.ip_address('127.0.0.1')
from socket import socket, AF_INET, SOCK_STREAM
s = socket(AF_INET, SOCK_STREAM)
try:
    s.connect((a, 8080))
except TypeError as e:
    print('s.connect((a, 8080))连接失败')
    s.connect((str(a), 8080))
    print('s.connect((str(a), 8080))连接成功')