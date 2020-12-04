#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
sys.argv 参数解析
"""

import sys

n = len(sys.argv)
print("Total arguments passed: ", n)

# Arguments passwd
print("\nName of Python script: ", sys.argv[0])

print("\nArguments passwd: ", end = " ")
for i in range(1, n):
    print(sys.argv[i], end = " ")
    
# Addition of numbers
Sum = 0
# Using argparse module
for i in range(1, n):
    Sum += int(sys.argv[i])
    
print("\n\nResult: ", Sum)
