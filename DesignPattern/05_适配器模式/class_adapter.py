#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
类适配器
"""
from adapder import WhatIHave

class WhatIWant:
    def required_function(self):
        pass 

class MyAdapter(WhatIHave, WhatIWant):
    def __init__(self, waht_i_have):
        self.what_i_have = waht_i_have
    
    def provided_function_1(self):
        return self.what_i_have.provided_function_1()

    def provided_function_2(self):
        return self.what_i_have.provided_function_2()

    def required_function(self):
        self.what_i_have.provided_function_1()
        self.what_i_have.provided_function_2()

class ClientObject(object):
    def __init__(self, what_i_want):
        self.what_i_want = what_i_want

    def do_something(self):
        self.what_i_want.required_function()


if __name__ == "__main__":
    adaptee = WhatIHave()
    adapter = MyAdapter(adaptee)
    client = ClientObject(adapter)

    client.do_something()