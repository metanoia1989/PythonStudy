#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from mysql import MySQL
import os
import requests
import json
from pathlib import Path
import sys
import settings

# 测试MySQL
db = MySQL(settings.DATABASE_HOST, settings.DATABASE_USERNAME, settings.DATABASE_PASSWORD, settings.DATABASE_NAME)

# 应用文件目录
curr_dir = os.path.dirname(os.path.realpath(__file__))
html_dir = os.path.join(curr_dir, "html")
if not os.path.exists(html_dir):
    os.mkdir(html_dir)
os.chdir(html_dir)

def fetch_chapter():
    """
    下载章节
    """


                

    
if __name__ == "__main__":
    pass