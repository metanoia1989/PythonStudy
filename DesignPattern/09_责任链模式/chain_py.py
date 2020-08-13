#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
责任链模式的Python实现
"""

class EndHandler(object):
    def __init__(self):
        pass

    def handle_request(self, request):
        pass

class Handler1(object):
    def __init__(self):
        self.next_handler = EndHandler()

    def handle_request(self, request):
        self.next_handler.handle_request(request)

def main(request):
    concrete_handler = Handler1()
    concrete_handler.handle_request(request)

if __name__ == "__main__":
    main(request)