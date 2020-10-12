#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MVC分离模式
"""
import sys

class GenericController(object):
    """
    控制器
    """
    def __init__(self):
        self.model = GenericModel()
        self.view = GenericView()

    def handle(self, request):
        data = self.model.get_data(request)
        self.view.generate_response(data)

class GenericModel(object):
    """
    模型
    """
    def __init__(self):
        pass

    def get_data(self, request):
        return { 'request': request }

class GenericView(object):
    def __init__(self):
        pass

    def generate_response(self, data):
        print(data)

if __name__ == "__main__":
    request_handler = GenericController()
    request_handler.handle(sys.argv[1])