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
json_dir = os.path.join(curr_dir, "json")

def create_category():
    """
    生成应用分类
    """
    for slug, name in cates.items():
        row = db.select_one("SELECT * FROM `spark_category` WHERE `slug`=%s", (slug))
        if row is None:
            db.execute("INSERT INTO `spark_category` (`slug`, `name`) VALUES(%s, %s)", (slug, name))

def download_json():
    """
    下载应用信息json文件
    """
    urls = [
        "https://json.jerrywang.top/store/network/applist.json",
        "https://json.jerrywang.top/store/chat/applist.json",
        "https://json.jerrywang.top/store/music/applist.json",
        "https://json.jerrywang.top/store/video/applist.json",
        "https://json.jerrywang.top/store/image_graphics/applist.json",
        "https://json.jerrywang.top/store/games/applist.json",
        "https://json.jerrywang.top/store/office/applist.json",
        "https://json.jerrywang.top/store/reading/applist.json",
        "https://json.jerrywang.top/store/development/applist.json",
        "https://json.jerrywang.top/store/tools/applist.json",
        "https://json.jerrywang.top/store/themes/applist.json",
        "https://json.jerrywang.top/store/others/applist.json",
    ]
    new_urls = dict(zip(cates.keys(), urls))
    
    if not os.path.exists(json_dir):
        os.mkdir(json_dir)
    os.chdir(json_dir)
    for key, url in new_urls.items():
        print("开始下载：{0} : {1}".format(key, url))
        filename = "{0}.json".format(key)
        # file_path = os.path.join(json_dir, filename)    
        # if not os.path.exists(file_path):
        response = requests.get(url)
        content = response.content.decode("utf-8")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        # else:
        #     print("文件{0}已存在，跳过".format(filename))
                

    
if __name__ == "__main__":
    pass