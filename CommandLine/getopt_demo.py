#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
getopt.getopt() 使用示例
"""

import getopt, sys

# 移除 sys.argv 中第一个脚本名参数      
argumentList = sys.argv[1:]

# 选项
options = "hmo:"

# 长选项
long_options = ["Help", "My_file", "Output = "]

try:
    # 解析处理命令行参数
    arguments, values = getopt.getopt(argumentList, options, long_options)
    # 检测每一个参数 类似Web框架的路由分发的概念
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h", "--help"):
            print("Displaying Help")
        elif currentArgument in ("-m", "--My_file"):
            print("Displaying file_name: ", sys.argv[0])
        elif currentArgument in ("-o", "--Output"):
            print("Enabling special output mode (% s)" % currentValue)
except getopt.error as err:
    print(str(err))