#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import requests
import json
from pathlib import Path
import sys
from redis import StrictRedis
from lxml.html import etree, tostring
import re

from mysql import MySQL
import settings
from utils import *

# 测试MySQL
db = MySQL(settings.DATABASE_HOST, settings.DATABASE_USERNAME, settings.DATABASE_PASSWORD, settings.DATABASE_NAME)
redis = StrictRedis()
PROCESSED_URLS = "processed_urls" # 已处理的url
CHAPTERS = "chapter_ids" # 所有章节的名称及ID

# 应用文件目录
curr_dir = os.path.dirname(os.path.realpath(__file__))
html_dir = os.path.join(curr_dir, "html")

# URL域名
BASE_URL = "http://www.chilin.edu.hk/edu/"

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
            print("没有调用请求")
            return f.read()
    else:
        print("没有缓存，请求", url)
        
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    #   'Cookie': settings.COOKIE 
    }
    proxies = {
        'http': 'http://localhost:10809',
        'https': 'http://localhost:10809',
    }

    response = requests.get(url, headers=headers, allow_redirects=True, proxies=proxies)
    response.encoding = "big5"
    html = response.text

    with open(filename, "w", encoding="utf8") as f:
        f.write(html)
    return html

def fetch_book():
    """
    下载整本书籍
    """
    url = "http://www.chilin.edu.hk/edu/report_section.asp?section_id=5"
    res = http_request(url)
    html = etree.HTML(res)

    # 所有的项目节点
    # links_li = html.xpath("//table[@class='content']/tobody/tr[3]/td[1]")
    # links_li = html.xpath("//table[@class='content']/tbody/tr/td/table/tbody/tr[3]/td[1]/table/tbody/tr/td[2]")
    links_li = html.xpath("//table[@class='content']//strong")
    chapters = [] 
    for li in links_li:
        values = li.xpath(".//text()")
        if (len(values) < 2):
            continue
        [ nu, name ]= values
        if nu.rstrip(".").find("5.1.") == -1:
            continue
        chapters.append(name.strip())

    # 插入章节
    for item in chapters:
        row = db.select_one("SELECT * FROM `book_chapter` WHERE `name`=%s", (item))
        if row is not None:
            print("{0} 章节已存在，无法插入！".format(item))
            redis.hset(CHAPTERS, row["name"], row["id"])
            continue
        sql = "INSERT INTO `book_chapter` ( `name`) VALUES (%s)"
        id = db.insert(sql, (item))
        redis.hset(CHAPTERS, item, id)

    # 提取所有章节的名称及内容
    links_li = html.xpath("//table[@class='content']//a")
    items = []
    for li in links_li:
        item = {
            "name":  li.xpath("./text()")[0],
            "url":   BASE_URL + li.xpath("./@href")[0]
        }
        if item["name"].find("志蓮淨苑禪修講座") != -1:
            break
        if item["name"].isspace():
            continue
        items.append(item)

    # 开始提取每个章节
    for chapter in items:
        print(chapter["name"], chapter["url"])
        fetch_chapter(chapter["name"], chapter["url"])

    
def fetch_chapter(chatper_name, url):
    """
    根据知识点来提取题目
    :chapter_name 章节名称
    :url string 章节url
    """
    print("章节提取开始：{0} {1}".format(chatper_name, url))

    if redis.exists(PROCESSED_URLS) and redis.sismember(PROCESSED_URLS, url):
        print("章节已处理，跳过")
        return

    res = http_request(url)
    html = etree.HTML(res)
    
    # 正则匹配题目数量
    try:
        number = html.xpath("//div[@id='1']/text()")[0]
        number = int(re.findall(r"共(\d+)题", number)[0]) 
    except IndexError:
        redis.sadd(PROCESSED_URLS, url) 
        print("此知识点没有题目")
        return

    items = [] 

    qhtml = html.xpath("//div[@class='dati']")[0]
    contents = qhtml.xpath("./b/text()") # 题目正文
    selects = qhtml.xpath("./ul") # 题目选项
    answers = qhtml.xpath("./div[@class='answer']") # 答案选项
    
    if len(selects) != number or len(contents) != number or len(answers) != number:
        redis.sadd(PROCESSED_URLS, url) 
        print("此知识点内容有误，请手动处理")
        redis.sadd("need_handle_urls", url) 
        return
    
    for i in range(0, number):
        # 提取选项 
        select_list =  selects[i].xpath("./li/text()")
        select_list = split_array(select_list, 2) 
        select_list = [ " ".join(x).replace("\u2003\u2002", "") for x in select_list ]

        # 提取答案
        answer_text = list(filter(lambda x : x != "您选择:",  answers[i].xpath(".//text()"))) 

        item = {
            "title": qhtml.xpath("./div[@id={0}]/text()".format(i+1)),
            "select": "\n".join(select_list),
            "content": contents[i],
            "answer": answer_text[0] + answer_text[1] + "\n".join(answer_text[2:]),
            "order": i + 1,
        }
        items.append(item)

    # 插入题目
    for item in items:
        if isinstance(item["title"], list):
            item["title"] = item["title"].pop()
        row = db.select_one("SELECT * FROM `tk_questions` WHERE `chapter_id`=%s and `title`=%s", (chapter_id, item["title"]))
        if row is not None:
            print("{0} 题目已存在，无法插入！".format(item["title"]))
            continue
        sql = """
            INSERT INTO `tk_questions` ( `chapter_id`, `title`, `content`, `select`, `answer`, `order`) 
            VALUES ( %s, %s, %s, %s, %s, %s)
        """
        data = (chapter_id, item["title"], item["content"], item["select"], item["answer"], item["order"])
        db.insert(sql, data)
        
    redis.sadd(PROCESSED_URLS, url) 
    print("此知识点题目提取完毕")



    
if __name__ == "__main__":
    init_env()

    # fetch_book()

    fetch_chapter("01 梵網經", "http://www.chilin.edu.hk/edu/report_section_detail.asp?section_id=59&id=490")
    
