#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python语言特性的策略模式
"""

class StrategyExecutor(object):
    def __init__(self, func=None):
        if func is not None:
            self.execute = func

    def execute(self, *args):
        print("Strategy not implementd ...")
    
def strategy_addition(arg1, arg2):
    print(arg1 + arg2)

def strategy_subtraction(arg1, arg2):
    print(arg1 - arg2)

if __name__ == "__main__":
    no_strategy = StrategyExecutor()
    addition_strategy = StrategyExecutor(strategy_addition)
    subtraction_strategy = StrategyExecutor(strategy_subtraction)

    no_strategy.execute(4, 6)
    addition_strategy.execute(4, 6)
    subtraction_strategy.execute(4, 6)