#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
职责分离
"""

import sys
import os

def get_append_write(filename):
    if os.path.exists(filename):
        return 'a'
    return 'w'

def name_in_file(filename, name):
    if not os.path.exists(filename):
        return False
    return name in read_names(filename)

def read_names(filename):
    with open(filename, 'r') as data_file:
        names = data_file.read().split('\n')
    return names
    
def write_name(filename, name):
    with open(filename, get_append_write(filename)) as data_file:
        data_file.write("{}\n".format(name))

def get_message(name):
    if name == "lion":
        return 'RRRrrrrroar!'

    if name_in_file('names.dat', name):
        print("Welcome back {}!".format(name))
    write_name('names.data', name)
    return "Hi {}, it is good to meet you".format(name)


name = sys.argv[1]
print(get_message(name))