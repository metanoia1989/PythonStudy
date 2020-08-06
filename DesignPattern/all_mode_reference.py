#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
设计模式快速参考：
* 单例模式
* 原型模式
* 工厂模式
* 建造者模式
* 适配器模式
* 装饰器模式
* 外观模式
* 代理模式
* 责任链模式
* 组合
* 命令模式
* 解释器模式
* 迭代器模式
* 观察者模式
* 状态模式
* 策略模式
* 模板方法模式
* 访问者模式
* 模型-视图-控制器模式
* 发布者-订阅者模式
"""

# 单例模式 Singleton
class SingletonObject(object):
    class __SingletonObject(object):
        def __init__(self):
            self.val = None 
        
        def __str__(self):
                return "{0!r} {1}".format(self, self.val)

    instance = None

    def __new__(cls):
        if not SingletonObject.instance:
            SingletonObject.instance = SingletonObject.__SingletonObject()
        return SingletonObject.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)

# 原型模式 Prototype
from abc import ABCMeta, abstractmethod
from copy import deepcopy

class Prototype(metaclass=ABCMeta):
    @abstractmethod
    def clone(self):
        pass

class Concrete(Prototype):
    def clone(self):
        return deepcopy(self)

# 工厂模式 Factory
from abc import ABCMeta, abstractmethod

class AbstractFactory(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def make_object(self):
        return

class ConcreteClass(object):
    pass

class ConcreteFactory(AbstractFactory):
    def make_object(self):
        return ConcreteClass()

# 建造者模式 Builder
from abc import ABCMeta, abstractmethod

class Director(object, metaclass=ABCMeta):
    def __init__(self):
        self._builder = None

    @abstractmethod
    def construct(self):
        pass

    def get_constructed_object(self):
        return self._builder.constructed_object

class Builder(object, metaclass=ABCMeta):
    def __init__(self, constructed_object):
        self.constructed_object = constructed_object

class Product(object):
    def __init__(self):
        pass

    def __repr__(self):
        pass

class ConcreteBuilder(Builder):
    pass

class ConcreteDirector(Director):
    pass

# 适配器
# third_party.py
class WhatIHave(object):
    def provided_function_1(self):
        pass

    def provided_function_2(self):
        pass

class WhatIWant(object):
    def required_function(self):
        pass

# adapter.py
class ObjectAdapter(object):
    def __init__(self, what_i_have):
        self.what_i_have = what_i_have

    def required_function(self):
        return self.what_i_have.provided_function_1()

    def __getattr__(self, attr):
        return getattr(self.what_i_have, attr)

# 装饰器 Decorator
from functools import wraps

def dummy_decorator(f):
    @wraps(f)
    def wrap_f():
        print("Function to be decorated: ", f.__name__)
        print("Nested wrapping function: ", wrap_f.__name__)
        return f()

    return wrap_f

@dummy_decorator
def do_nothing():
    print("Inside do_nothing") 

if __name__ == "__main__":
    print("Wrapped function: ", do_nothing.__name__)
    do_nothing()

# 外观模式 Facade
class Invoice(object):
    def __init__(self, customer):
        pass

class Customer(object):
    def __init__(self, customer_id):
        pass

class Item:
    def __init__(self, item_barcode):
        pass

class Facade(object):
    @staticmethod
    def make_invoice(customer):
        return Invoice(customer)

    @staticmethod
    def make_customer(customer_id):
        return Customer(customer_id)

    @staticmethod
    def make_item(item_barcode):
        return Item(item_barcode)

# 代理模式 Proxy
import time

class RawClass(object):
    def func(self, n):
        return f(n)

def memoize(fn):
    __cache = {}

    def memoized(*args):
        key = (fn.__name__, args)        
        if key in __cache:
            return __cache[key]
        __cache[key] = fn(*args)
        return __cache[key]

class ClassProxy(object):
    def __init__(self, target):
        self.target = target

        func = getattr(self.target, 'func')
        setattr(self.target, 'func', memoize(func))

    def __getattr__(self, name):
        return getattr(self.target, name)

# 责任链 chain of responsibility
class EndHandler(object):
    def __init__(self):
        pass

    def handle_request(self, request):
        pass 

class Handler1(object):
    def __init__(self):
        self.next_handler = EndHandler()

    def handler_request(self, request):
        self.next_handler.handle_request(request)

def main(request):
    concrete_handler = Handler1()
    concrete_handler.handler_request(request)

if __name__ == "__main__":
    main(request)

# 责任链可选实现
class Dispatcher(object):
    def __init__(self, handlers=[]):
        self.handlers = handlers

    def handle_request(self, request):
        for handler in self.handlers:
            request = handler(request)
        return request

# 命令模式 Command
class Command(object):
    def __init__(self, receiver, text):
        self.receiver = receiver
        self.text = text

    def execute(self):
        self.receiver.print_message(self.text)

class Receiver(object):
    def print_message(self, text):
        print("Message received: {}".format(text))

class Invoker(object):
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def run(self):
        for command in self.commands:
            command.execute()
        
if __name__ == "__main__":
    receiver = Receiver()
    command1 = Command(receiver, "Execute Command 1")
    command2 = Command(receiver, "Execute Command 2")

    invoker = Invoker()
    invoker.add_command(command1)
    invoker.add_command(command2)
    invoker.run()

# 组合 Composite
class Leaf(object):
    def __init__(self, *args, **kwargs):
        pass

    def component_function(self):
        print("Leaf")

class Composite(object):
    def __init__(self, *args, **kwargs):
        self.children = []

    def component_function(self):
        for child in self.children:
            child.component_function()

    def add(self, child):
        self.children.append(child)

    def remove(self, child):
        self.children.remove(child)

# 解释器 interpreter
class NotTerminal(object):
    def __init__(self, expression):
        self.expression = expression

    def interpret(self):
        self.expression.interpret()

class Terminal(object):
    def interpret(self):
        pass

# 迭代器 Iterator
from abc import ABCMeta, abstractmethod

class Iterator(object, metaclass=ABCMeta):
    @abstractmethod
    def has_next(self):
        pass

    @abstractmethod
    def next(self):
        pass

class Container(metaclass=ABCMeta):
    @abstractmethod
    def getIterator(self):
        pass

class MyListIterator(Iterator):
    def __init__(self, my_list):
        self.index = 0
        self.list = my_list.list

    def has_next(self):
        return self.index < len(self.list)

    def next(self):
        self.index += 1
        return self.list[self.index - 1]

class MyList(Container):
    def __init__(self, *args):
        self.list = list(args) 

    def getIterator(self):
        return MyListIterator(self)

if __name__ == "__main__":
    my_list = MyList(1, 2, 3, 4, 5, 6)
    my_iterator = my_list.getIterator()

    while my_iterator.has_next():
        print(my_iterator.next())

    # for element in collection
    #     do_something(element)

# 观察者模式 Observer
class ConcreteObserver(object):
    def update(self, observed):
        print("Observing: {}".format(observed))

class Observable(object):
    def __init__(self):
        self.callbacks = set()
        self.changed = False

    def register(self, callback):
        self.callbacks.add(callback)

    def unregister(self, callback):
        self.callbacks.discard(callback)

    def unregister_all(self):
        self.callbacks = set()

    def poll_for_change(self):
        if self.changed:
            self.update_all()

    def update_all(self):
        for callback for in self.callbacks:
            callback(self)

# 状态模式 State
class State(object):
    pass

class ConcreteState(State):
    def __init__(self, state_machine):
        self.state_machine = state_machine

    def switch_state(self):
        self.state_machine.state = self.state_machine.state2

class ConcreteState2(State):
    def __init__(self, state_machine):
        self.state_machine = state_machine

    def switch_state(self):
        self.state_machine.state = self.state_machine.state1

class StateMachine(object):
    def __init__(self):
        self.state1 = ConcreteState1(self)
        self.state2 = ConcreteState2(self)
        self.state = self.state1

    def switch(self):
        self.state.switch_state()

    def __str__(self):
        return str(self.state)

def main():
    state_machine = StateMachine()
    print(state_machine)

    state_machine.switch()
    print(state_machine)

if __name__ == "__main__":
    main()


# 策略模式 Strategy
def executor(arg1, arg2, func=None):
    if func is None:
        return "Strategy not implemented..."
    return func(arg1, arg2)

def strategy_1(arg1, arg2):
    return f_1(arg1, arg2)

def strategy_2(arg1, arg2):
    return f_2(arg1, arg2)
    

# 模板方法 Template method
from abc import ABCMeta, abstractmethod

class TemplateAbstractBaseClass(metaclass=ABCMeta):
    def template_method(self):
        self._step_1()
        self._step_2()
        self._step_n()

    @abstractmethod
    def _step_1(self):
        pass

    @abstractmethod
    def _step_2(self):
        pass

    @abstractmethod
    def _step_n(self):
        pass

class ConcreteImplementationClass(TemplateAbstractBaseClass):
    def _step_1(self):
        pass
    
    def _step_2(self):
        pass

    def _step_3(self):
        pass

# 访问者模式 Visitor
from abc import ABCMeta, abstractmethod

class Visitable(object):
    def accept(self, visitor):
        visitor.visit(self) 

class CompositeVisitable(Visitable):
    def __init__(self, iterable):
        self.iterable = iterable

    def accept(self, visitor):
        for element in self.iterable:
            element.accept(visitor)
        
        visitor.visit(self)

class AbstractVisitor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def visit(self, element):
        raise NotImplementedError("A visitor need to define a visit method")

class ConcreteVisitable(Visitable):
    def __init__(self):
        pass

class ConcreteVisitor(AbstractVisitor):
    def visit(self, element):
        pass

# 模型-视图-控制器 MVC
import sys

class GenericController(object):
    def __init__(self):
        self.model = GenericModel()
        self.view = GenericView()

    def handle(self, request):
        data = self.model.get_data(request)
        self.view.generate_response(data)

class GenericModel(object):
    def __init__(self):
        pass

    def get_data(self, request):
        return { 'request': request }

class GenericView(object):
    def __init__(self):
        pass

    def generate_response(self, data):
        print(data)

def main(name):
    request_handler = GenericController()
    request_handler.handle(name)

if __name__ == "__main__":
    main(sys.argv[1])

# 发布者-订阅者
class Message(object):
    def __init__(self):
        self.payload = None
        self.topic = "all"

class Subscriber(object):
    def __init__(self, dispatcher, topic):
        dispatcher.subscribe(self, topic)

    def process(self, message):
        print("Message: {}".format(messgae.payload))

class Publisher(object):
    def __init__(self, dispatcher):
        self.dipatcher = dispatcher
    
    def publish(self, message):
        self.dipatcher.send(message)

class Dispatcher(object):
    def __init__(self):
        self.topic_subscribes = dict()

    def subscribe(self, subscriber, topic):
        self.topic_subscribes.setdefault(topic, set()).add(subscriber)

    def unsubscribe(self, subscriber, topic):
        self.topic_subscribes.setdefault(topic, set()).discard(subscriber) 

    def unsubscribe_all(self, topic):
        self.subscribes = self.topic_subscribes[topic] = set()

    def send(self, message):
        for Subscriber in self.topic_subscribes[message.topic]:
            Subscriber.process(message)