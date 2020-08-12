#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
糟糕的调用演示
"""

def function_1(in_string):
    print("function_1")
    return "".join([x for x in in_string if x != '1'])

def function_2(in_string):
    print("function_2")
    return "".join([x for x in in_string if x != '2'])

def function_3(in_string):
    print("function_3")
    return "".join([x for x in in_string if x != '3'])

def function_4(in_string):
    print("function_4")
    return "".join([x for x in in_string if x != '4'])

def main_function(input_string):
    if '1' in input_string:
        input_string = function_1(input_string)
    if '2' in input_string:
        input_string = function_2(input_string)
    if '3' in input_string:
        input_string = function_3(input_string)
    if '4' in input_string:
        input_string = function_4(input_string)
    print(input_string)

if __name__ == "__main__":
    main_function("1221345439")