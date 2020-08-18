#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单的观察者模式
"""

from abc import ABCMeta, abstractmethod

class Observer(object, metaclass=ABCMeta):
    
    @abstractmethod
    def update(self, observed):
        pass

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

