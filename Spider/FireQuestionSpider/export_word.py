#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
from pathlib import Path
import sys

from mysql import MySQL
import settings
from utils import *

# 测试MySQL
db = MySQL(settings.DATABASE_HOST, settings.DATABASE_USERNAME, settings.DATABASE_PASSWORD, settings.DATABASE_NAME)

# 应用文件目录
curr_dir = os.path.dirname(os.path.realpath(__file__))
word_dir = os.path.join(curr_dir, "word")

def init_env():
    """ 
    初始化环境
    """ 
    # 创建缓存目录
    if not os.path.exists(word_dir):
        os.mkdir(word_dir)
    os.chdir(word_dir)
    
if __name__ == "__main__":
    init_env()