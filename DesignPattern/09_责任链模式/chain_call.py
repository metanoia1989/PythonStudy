#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
链式调用
"""

class CatchAll(object):
    """
    接口类
    """
    def __init__(self):
        self.next_to_execute = None

    def execute(self, request):
        print("end reached.")
        print(request)

class Function1Class(object):
    def __init__(self):
        self.next_to_execute = CatchAll()

    def execute(self, request):
        print("function_1")
        print(request)
        request = "".join([x for x in request if x != '1'])
        self.next_to_execute.execute(request)

class Function2Class(object):
    def __init__(self):
        self.next_to_execute = CatchAll()

    def execute(self, request):
        print("function_2")
        print(request)
        request = "".join([x for x in request if x != '2'])
        self.next_to_execute.execute(request)

class Function3Class(object):
    def __init__(self):
        self.next_to_execute = CatchAll()

    def execute(self, request):
        print("function_3")
        print(request)
        request = "".join([x for x in request if x != '3'])
        self.next_to_execute.execute(request)

class Function4Class(object):
    def __init__(self):
        self.next_to_execute = CatchAll()

    def execute(self, request):
        print("function_4")
        print(request)
        request = "".join([x for x in request if x != '4'])
        self.next_to_execute.execute(request)

def main_function(head, request):
    head.execute(request)

if __name__ == "__main__":
    hd = Function1Class()

    current = hd
    current.next_to_execute = Function2Class()

    current = current.next_to_execute
    current.next_to_execute = Function3Class()

    current = current.next_to_execute
    current.next_to_execute = Function4Class()

    main_function(hd, "1221345439")