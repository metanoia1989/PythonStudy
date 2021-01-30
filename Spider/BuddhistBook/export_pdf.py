#!/usr/bin/env python3
#-*- coding: utf-8 -*-  


import os
import sys

from jinja2 import FileSystemLoader, Environment
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration

from mysql import MySQL
import settings
from utils import *

# 测试MySQL
db = MySQL(settings.DATABASE_HOST, settings.DATABASE_USERNAME, settings.DATABASE_PASSWORD, settings.DATABASE_NAME)

# 应用文件目录
curr_dir = os.path.dirname(os.path.realpath(__file__))
BOOK_NAME = "巴利文佛典選譯"

def export_pdf():
    """
    导出所有经文为PDF
    """ 
    # 查询所有章节
    sql = "SELECT id, name from `book_chapter`"
    chapters = db.select_all(sql)
    
    # 查询章节对应的经文
    for i, item in enumerate(chapters):
        sql = "SELECT id, CONCAT(`order`, ' ', `title`) as name, `content` from `book_article` WHERE chapter_id = %s"
        articles = db.select_all(sql, (str(item["id"])))
        chapters[i]["child"] = articles

    # weasyprint 是从HTML输出PDF的，所以要先用Jinja2模板引擎构建HTML，
    templateEnv = Environment(loader = FileSystemLoader(searchpath=curr_dir))
    template = templateEnv.get_template("template.html")
    html = template.render(items=chapters)

    filename = curr_dir + "/" + BOOK_NAME + ".pdf"
    print(filename)
    HTML(string=html).write_pdf(filename) 

if __name__ == "__main__":
    export_pdf()
