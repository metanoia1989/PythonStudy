#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
发布-订阅者模式
"""

class Message(object):
    def __init__(self):
        self.payload = None

class Subscriber(object):
    def process(self, message):
        print("Message: {}".format(message.payload))

class Publisher(object):
    def __init__(self):
        self.subscribers = set()
        self.changed = False

    def subscribe(self, subscriber):
        self.subscribers.add(subscriber)

    def unsubscribe(self, subscriber):
        self.subscribers.discard(subscriber)

    def unsubscribe_all(self):
        self.subscribers = set()


    def publish(self, message):
        for subscriber in self.subscribers:
            subscriber.process(message)
