#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
argparse 模块选项
"""
import argparse

# 初始化解析器
parser = argparse.ArgumentParser(description="命令行工具描述")
parser.add_argument("-o", "--Output", help="展示输出")
args =  parser.parse_args()

if args.Output:
    print("展示输出 %s" % args.Output)