#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class GreetingView(object):
    def __init__(self):
        pass

    def generate_greeting(self, name, time_of_day, known):
        if name == "lion":
            print("RRRrrrroar!")
            return
        if known:
            print("Good {} welcome back {}!".format(time_of_day, name))
        else:
            print("Good {} {}, it is good to meet you".format(time_of_day, name))