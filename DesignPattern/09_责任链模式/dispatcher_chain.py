#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
实例化一个主对象，以便在实例化时将处理程序从被传递到调度器的列表中分离出来
"""

class Dispatcher(object):
    def __init__(self, handlers = []):
        self.handlers = handlers

    def handle_request(self, request):
        for handler in self.handlers:
            request = handler(request)

        return request

def function_1(in_string):
    print("function_1: {}".format(in_string))
    return "".join([x for x in in_string if x != '1'])

def function_2(in_string):
    print("function_2: {}".format(in_string))
    return "".join([x for x in in_string if x != '2'])

def function_3(in_string):
    print("function_3: {}".format(in_string))
    return "".join([x for x in in_string if x != '3'])

def function_4(in_string):
    print("function_4: {}".format(in_string))
    return "".join([x for x in in_string if x != '4'])

def main_function(request):
    dispatcher = Dispatcher([
        function_1,
        function_2,
        function_3,
        function_4
    ])
    dispatcher.handle_request(request)

if __name__ == "__main__":
    main_function("1221345439")