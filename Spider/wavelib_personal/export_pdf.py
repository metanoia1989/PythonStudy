#!/usr/bin/env python3
#-*- coding: utf-8 -*-  


import os
import sys

from datetime import datetime

from jinja2 import FileSystemLoader, Environment
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration

from mysql import MySQL
import settings

# 测试MySQL
db = MySQL(settings.DATABASE_HOST, settings.DATABASE_USERNAME, settings.DATABASE_PASSWORD, settings.DATABASE_NAME)

# 应用文件目录
curr_dir = os.path.dirname(os.path.realpath(__file__))
BOOK_NAME = "微澜图书馆人才"

def filter_person(item):
    item["addtime"] =  datetime.fromtimestamp(int(item["addtime"])).strftime('%Y-%m-%d')
    item["uptime"] =  datetime.fromtimestamp(int(item["uptime"])).strftime('%Y-%m-%d')
    return item

def export_pdf():
    # 查询所有章节
    sql = "SELECT username, sex, province, city, how, about, `addtime`, uptime, birth FROM ts_user_info"
    persons = db.select_all(sql)
    
    persons = list(filter(lambda item: item["about"] != "", persons))
    persons = list(map(filter_person, persons))

    # weasyprint 是从HTML输出PDF的，所以要先用Jinja2模板引擎构建HTML，
    templateEnv = Environment(loader = FileSystemLoader(searchpath=curr_dir))
    template = templateEnv.get_template("template.html")
    html = template.render(items=persons)

    filename = curr_dir + "/" + BOOK_NAME + ".pdf"

    print(filename)
    HTML(string=html).write_pdf(filename) 

if __name__ == "__main__":
    export_pdf()
