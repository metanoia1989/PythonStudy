# 协程
协程是一种比进程和线程更加轻量级的解决方案，也通过yield实现了协程，但最大的疑问是没有提供像进程或线程类的任务调度，没有体现出协程的优势。

- [协程与多任务调度](https://www.hitoy.org/coroutine-multitasking-schedule.html)


# 异常
- [Python Standard Exceptions](http://www.tutorialspoint.com/python/standard_exceptions.htm)

异常(exceptions)是Python中一种非常重要的类型，它和语法错误不同，是在程序运行期间引发的错误。

内置异常：IOError,NameError,KeyboardInterrupt

Python的异常可以通过try语句来检查，任何在try语句块里的代码都会被监测，检查有无异常产生，except会根据输入检查异常的类型，并执行except内的代码。

except后面的两个参数: 错误的类型, Exception的实例.

用raise抛出异常
finally 无论是否捕获异常 都会执行

自定义异常，所有异常必须直接或者间接的继承自Exception类。
```python
#!/usr/bin/env python
class MyError(Exception):
    def __init__(self,*args):
        self.value=args[0]
    def __str__(self):
        return repr(self.value)
def showname(*args):
    if args:
        print args
    else:
        raise MyError('Error: need 1 arguments at last, 0 Input')
```
