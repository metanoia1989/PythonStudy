#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from prototype import Prototype
from copy import deepcopy

"""
原型模式的具体实现使用
"""

class Concrete(Prototype):
    def clone(self):
        return deepcopy(self)