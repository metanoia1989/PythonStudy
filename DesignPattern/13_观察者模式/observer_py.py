#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
观察者模式 鸭子类型 Python版
"""

class ConcreteObserver(Observer):
    def update(self, observed):
        print("Observing: " + observed)

class Observable(object):
    def __init__(self):
        self.observers = set()

    def register(self, observer):
        self.observers.add(observer)

    def unregister(self, observer):
        self.observers.discard(observer)

    def unregister_all(self):
        self.observers = set()

    def update_all(self):
        for observer in self.observers:
            observer.update(self)

