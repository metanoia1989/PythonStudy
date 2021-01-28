#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import requests
from pathlib import Path
import sys
from lxml.html import etree
import re
from jinja2 import FileSystemLoader, Environment
import json
from weasyprint import HTML, CSS


from utils import *

# 测试MySQL
PROCESSED_URLS = "processed_urls" # 已处理的url

# 应用文件目录
curr_dir = os.path.dirname(os.path.realpath(__file__))
html_dir = os.path.join(curr_dir, "html")

# URL域名
BASE_URL = "https://www.un.org/chinese/esa/education/lifelonglearning/"

BOOK_NAME = "教育-财富蕴藏其中"

def init_env():
    """ 
    初始化环境
    """ 
    # 创建缓存目录
    if not os.path.exists(html_dir):
        os.mkdir(html_dir)
    os.chdir(html_dir)


def http_request(url):
    """
    发起get请求，请求的内容会缓存到文件中   
    """
    filename = url_to_file(url)
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf8") as f:
            print("已缓存 没有调用请求")
            return f.read()
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    }
    response = requests.get(url, headers=headers, allow_redirects=True)
    response.encoding = "gbk"
    html = response.text

    with open(filename, "w", encoding="utf8") as f:
        f.write(html)
    return html

def fetch_book():
    """
    提取整本书籍  https://www.un.org/chinese/esa/education/lifelonglearning/index.html     
    有多个章节，除了概要章节外，其他的章节都有子章节    
    """
    url = "https://www.un.org/chinese/esa/education/lifelonglearning/index.html"
    res = http_request(url)
    html = etree.HTML(res)

    # 所有的项目节点
    links = html.xpath("//dl[@class='nav3-grid'][1]/dt/a")
    projects = []
    for li in links:
        projects.append({
            "name":  li.xpath("./text()")[0],
            "url":   BASE_URL + li.xpath("./@href")[0]
        })

    # 提取每个章节的子章节
    for i in range(len(projects)):
        item = projects[i]
        print("下载章节：{0} {1}".format(item["name"], item["url"]))
        projects[i] = fetch_chapter(item["name"], item["url"])
    
    # 转换为PDF
    export_pdf(projects)
    
    
def fetch_chapter(chapter_name, url):
    """
    提取章节的简述，以及子章节内容，并且将提取的章节内容返回

    :chapter_name string 章节名称
    :url string 章节链接
    """
    res = http_request(url)
    html = etree.HTML(res)
    
    item = {
        "name": chapter_name,
        "url": url,
    }
    # 提取章节简述
    contents = html.xpath("//div[@class='column1-unit'][1]//text()")
    item["content"] = "\n".join(list(filter(lambda x: not x.isspace(), contents))) 
    
    # 提取子章节内容
    links = html.xpath("//dl[@class='nav3-grid'][1]//dd/a")
    item["children"] = []
    for li in links:
        child = {
            "name":  li.xpath("./text()")[0],
            "url":   BASE_URL + li.xpath("./@href")[0]
        }
        print("下载章节：{0}  {1}".format(child["name"], child["url"]))
        childHtml = etree.HTML(http_request(child["url"]))
        childContents = html.xpath("//div[@class='column1-unit'][1]//text()")
        child["content"] = "\n".join(list(filter(lambda x: not x.isspace(), childContents))) 
        item["children"].append(child)

    return item

def export_pdf(items):
    """ 
    将提取好的数据转换为 PDF
    :items list 存储着章节数据的列表
    """ 
    # weasyprint 是从HTML输出PDF的，所以要先用Jinja2模板引擎构建HTML，
    templateEnv = Environment(loader = FileSystemLoader(searchpath=curr_dir))
    template = templateEnv.get_template("template.html")
    html = template.render(items=items)
    
    # with open("outout.html", "w", encoding="utf-8") as f:
    #     f.write(html)
    # sys.exit(0)
    
    # cssString = """
    # """
    # css = CSS(cssString)

    filename = curr_dir + "/" + BOOK_NAME + ".pdf"
    print(filename)
    HTML(string=html).write_pdf(filename) 

    
if __name__ == "__main__":
    init_env()

    fetch_book()
    
    
