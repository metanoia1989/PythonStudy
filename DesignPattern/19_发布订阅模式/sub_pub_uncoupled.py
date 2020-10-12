#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
发布订阅模式 - 解耦合
所有的消息，通过分发器类传递
发布者和订阅者的数量可以任意变化
但是发布者和分发器是强依赖关系
"""

class Message(object):
    def __init__(self):
        self.payload = None

class Subscriber(object):
    def __init__(self, dispathcher):
        dispathcher.subscribe(self)

    def process(self, message):
        print("Message: {}".format(message.payload))

class Publisher(object):
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
    
    def publish(self, message)
        self.dispatcher.send(message)

class Dispatcher(object):
    def __init__(self):
        self.subscribers = set()

    def subscribe(self, subscriber):
        self.subscribers.add(subscriber)

    def unsubscribe(self, subscriber):
        self.subscribers.discard(subscriber)

    def unsubscribe_all(self):
        self.subscribers = set()

    def send(self, message):
        for subscriber in self.subscribers:
            subscriber.process(message)
