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
redis = StrictRedis(charset="utf-8", decode_responses=True)
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
        'http': 'http://127.0.0.1:10809',
        'https': 'http://127.0.0.1:10809',
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

    
def fetch_chapter(chapter_name, url):
    """
    根据知识点来提取题目
    :chapter_name 经文名
    :url string 章节url
    """
    print("经文提取开始：{0} {1}".format(chapter_name, url))

    if redis.exists(PROCESSED_URLS) and redis.sismember(PROCESSED_URLS, url):
        print("经文已处理，跳过")
        return

    res = http_request(url)
    html = etree.HTML(res)
    
    # 提取卷名
    chapter_names = "|".join(redis.hkeys(CHAPTERS))
    volume = " ".join(html.xpath("//table[@class='content']//p[1]//text()")) 
    if volume.isspace() or len(volume) == 0:
        # =_= 当页面没有p的时候，就只能全文匹配了，贼恶心
        volume = " ".join(html.xpath("//table[@class='content']//text()")) 
        
    try:
        volume = re.search(r"({0})".format(chapter_names), volume).group()
    except Exception as e:
        volume = "小部"
        
    volume_id = redis.hget(CHAPTERS, volume)

    # 提取内容
    content = html.xpath("//table[@class='content']//p//text()")
    content = "\n".join(list(filter(lambda x: x != "\u3000\u3000", content)))
    [ order, title] = re.search(r"(\d+-?\d?)\s+(.*)$", chapter_name).groups()

    item = {
        "title": title,
        "order": order,
        "chapter_id": volume_id,
        "content": ""
    }

    contents = []
    contents.append(content)

    # 提取其他几页
    LINK_PAGE_BASE = "http://www.chilin.edu.hk/edu/report_section_detail.asp"
    links = html.xpath("//td[@class='subtitle'][1]")[0].xpath("./following-sibling::td[1]//a//@href")
    links = list(map(lambda x : LINK_PAGE_BASE + x, links))
    for link in links:
        res = http_request(link)
        html = etree.HTML(res)
        content = html.xpath("//table[@class='content']//p//text()")
        if len(content) == 0:
            content = html.xpath("//table[@class='content']//td/text()")
            content = list(filter(lambda x: x == "\u3000\u3000" or not x.replace("|","").isspace(), content))[1:]
             
        content = "\n".join(list(map(lambda x: "\n" if x == "\u3000\u3000" else x , content)))
        contents.append(content)

    item["content"] = "\n".join(contents) 

    # 插入经文
    row = db.select_one("SELECT * FROM `book_article` WHERE `chapter_id`=%s and `title`=%s", (volume_id, item["title"]))
    if row is not None:
        print("{0} 经文已存在，无法插入！".format(item["title"]))
        redis.sadd(PROCESSED_URLS, url) 
        return
    
    sql = """
        INSERT INTO `book_article` ( `chapter_id`, `title`, `content`, `order`) 
        VALUES ( %s, %s, %s, %s)
    """
    data = (volume_id, item["title"], item["content"], item["order"])
    db.insert(sql, data)
        
    redis.sadd(PROCESSED_URLS, url) 
    print("此经文已插入完毕")


    
if __name__ == "__main__":
    init_env()

    fetch_book()

    # fetch_chapter("01 梵網經", "http://www.chilin.edu.hk/edu/report_section_detail.asp?section_id=59&id=490")

    # 经文名间有多个空格
    # fetch_chapter("02   沙門果經", "http://www.chilin.edu.hk/edu/report_section_detail.asp?section_id=59&id=272")
    
    # 提取不到卷名
    # fetch_chapter("02 天子相應", "http://www.chilin.edu.hk/edu/report_section_detail.asp?section_id=61&id=573")
    # 正则匹配卷名失败
    # fetch_chapter("30 相經", "http://www.chilin.edu.hk/edu/report_section_detail.asp?section_id=59&id=545")
    # fetch_chapter("08 第八集 (部份經文)", "http://www.chilin.edu.hk/edu/report_section_detail.asp?section_id=62&id=338")
    
    # 提取经名和序号错误
    # 有重复的请求
    # fetch_chapter("12-2  因緣相應 （續）", "http://www.chilin.edu.hk/edu/report_section_detail.asp?section_id=61&id=278")

    
