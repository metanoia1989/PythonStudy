#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class StrategyExecutor(object):
    def __init__(self, strategy=None):
        self.strategy = strategy

    def execute(self, arg1, arg2):
        if self.strategy is None:
            print("Strategy not implementd ...")
        else:
            self.strategy.execute(arg1, arg2)

class AdditionStrategy(object):
    def execute(self, arg1, arg2):
        print(arg1 + arg2)

class SubstractStrategy(object):
    def execute(self, arg1, arg2):
        print(arg1 - arg2)

if __name__ == "__main__":
    no_strategy = StrategyExecutor()
    addition_strategy = StrategyExecutor(AdditionStrategy())
    subtraction_strategy = StrategyExecutor(SubstractStrategy())

    no_strategy.execute(4, 6)
    addition_strategy.execute(4, 6)
    subtraction_strategy.execute(4, 6)