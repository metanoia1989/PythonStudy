#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单的网络APP
"""

import sys

name = sys.argv[1]

try:
    with open('names.dat', 'r') as data_file:
        names = [ x for x in data_file.readlines() ]
except FileNotFoundError as e:
    with open('names.dat', 'w') as data_file:
        data_file.write(name)
    names = []

if name in names:
    print("Welcome back {}!".format(name))
else:
    print("Hi {}, it is good to meet you".format(name))
    with open("names.dat", "a") as data_file:
        data_file.write(name)