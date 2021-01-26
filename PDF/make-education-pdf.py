#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
教育：财富蕴含其中   https://www.un.org/chinese/esa/education/lifelonglearning/index.html
"""

import os.path
import os
from pathlib import Path

BASE_DIR = Path(os.getcwd()).joinpath("cache") 
if not BASE_DIR.exists():
    os.makedirs(BASE_DIR)

os.chdir(BASE_DIR.absolute());    


"""
爬取思路：
为了提高性能进行缓存处理，每爬取一个都存入缓存，用文件缓存，并且用 redis 缓存

"""