#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
保留被装饰函数的 __name__ 和 __doc__
"""

def dummy_decorator(f):
    def wrap_f():
        print("Function to be decorated: ", f.__name__)
        print("Nested wrapping function: ", wrap_f.__name__)
        return f()

    return wrap_f

@dummy_decorator
def do_noting():
    print("Inside do_nothing")

if __name__ == "__main__":
    print("Wrapped function: ", do_noting.__name__)
    do_noting()