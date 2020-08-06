#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class WhatIHave(object):
    def provided_function_1(self):
        pass

    def provided_function_2(self):
        pass

class WhatIWant(object):
    def required_function(self):
        pass

class Client(object):
    def __init__(self, some_object):
        self.some_object = some_object

    def do_something(self):
        """
        用简单的if else 来适配对象
        """
        if self.some_object.__class__ == WhatIHave:
            self.some_object.provided_function_2()
            self.some_object.provided_function_1()
        elif self.some_object.__class__ == WhatIWant:
            self.some_object.required_function()
        else:
            print("Class of self.some_object not recognized")