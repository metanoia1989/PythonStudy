#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
发布订阅模式 - 特定的主题
"""

class Message(object):
    def __init__(self):
        self.payload = None
        self.topic = "all"

class Subscriber(object):
    def __init__(self, dispathcher, topic):
        dispathcher.subscribe(self, topic)

    def process(self, message):
        print("Message: {}".format(message.payload))

class Publisher(object):
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
    
    def publish(self, message):
        self.dispatcher.send(message)

class Dispatcher(object):
    def __init__(self):
        self.topic_subscribers = dict()

    def subscribe(self, subscriber, topic):
        self.topic_subscribers.setdefault(topic, set()).add(subscriber)

    def unsubscribe(self, subscriber, topic):
        self.topic_subscribers.setdefault(topic, set()).discard(subscriber)

    def unsubscribe_all(self, topic):
        self.topic_subscribers[topic] = set()

    def send(self, message):
        for subscriber in self.topic_subscribers[message.topic]:
            subscriber.process(message)

if __name__ == "__main__":
    dispatcher = Dispatcher()

    publisher_1 = Publisher(dispatcher)
    subcriber_1 = Subscriber(dispatcher, 'topic1')

    message = Message()
    message.payload = "My Payload"
    message.topic = "topic1"

    publisher_1.publish(message)