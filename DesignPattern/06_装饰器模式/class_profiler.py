#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
可以同时装饰类和函数的装饰器
"""
import time

def profiling_wrapper(f):
    @wraps(f) 
    def wrap_f(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **args)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("[Time elapsed for n = {}] {}".format(n, elapsed_time))
        return result

    return wrap_f

def profile_all_class_methods(Cls):
    class ProfiledClass(object):
        def __init__(self, *args, **kwargs):
          self.inst = Cls(*args, **kwargs)

        def __getattribute__(self, name):
            try:
                x = super().__getattribute__(name)
            except AttributeError:
                pass
            else:
                x = self.inst.__getattribute__(name)
                if type(x) == type(self.__init__):
                    return profiling_wrapper(x)
                else:
                    return x
            
    return ProfiledClass

@profile_all_class_methods
class DoMathStuff(object):
    def fib(self):
        pass

    @profile_decorator
    def factorial(self):
        pass