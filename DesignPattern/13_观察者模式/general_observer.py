#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

class ConcreteObserver(object):
    def update(self, observed):
        print("Observing: {}".format(observed))

class Observable(object):
    def __init__(self):
        self.callbacks = set()
        self.changed = False

    def register(self, callback):
        self.callbacks.add(callback)

    def unregister(self, observer):
        self.callbacks.discard(observer)

    def unregister_all(self):
        self.callbacks = set()

    def poll_for_change(self):
        if self.changed:
            self.update_all()

    def update_all(self):
        for callback in self.callbacks:
            callback(self)

if __name__ == "__main__":
    observed = Observable()
    observer1 = ConcreteObserver()

    observed.register(lambda x: observer1.update(x))
    # observed.update_all()

    while True:
        time.sleep(2)
        observed.poll_for_change()
        observed.changed = True