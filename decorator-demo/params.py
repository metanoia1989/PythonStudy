from functools import wraps
import logging

def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + "was called")
        return func(*args, **kwargs) # 这里的意思是 调用 func ，并返回 func 的返回值， 好迷惑人啊，简写到这个地步你妹啊
    return with_logging

def addition_func(x):
    """Do some math."""
    return x + x

addition_func = logit(addition_func) 
# 等同于 ==> addtion_func == with_logging
# addtion_func(4) ==> with_loggin(4) ==>  return_var = addtion_func(4) ; return return_var
result = addition_func(4)
print(result)



def use_logging(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level == "warn":
                logging.warn("%s is running" % func.__name__)
            elif level == "info":
                logging.info("%s is running" % func.__name__)
            return func(*args)
        return wrapper

    return decorator

@use_logging(level="warn") # 这里已经进行了一次函数调用，即调用了 use_loging(level="warn")，把 decorator 作为装饰器
def foo(name='foo'):
    print("i am %s" % name)

"""
上面三行的代码等同于
@decorator 
def foo(name='foo'):
    print("i am %s" % name)
即
foo = decorator(foo) # 并且传入了一个变量 level="warn"
foo = wrapper(name='foo')  = 执行添加的功能 + foo(name='foo')
"""

foo()