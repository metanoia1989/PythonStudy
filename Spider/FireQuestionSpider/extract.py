#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import requests
import json
from pathlib import Path
import sys
from redis import StrictRedis
from lxml.html import etree
import re

from mysql import MySQL
import settings
from utils import *

# 测试MySQL
db = MySQL(settings.DATABASE_HOST, settings.DATABASE_USERNAME, settings.DATABASE_PASSWORD, settings.DATABASE_NAME)
redis = StrictRedis()
CACHED_URLS = "cacheed_urls" # 已缓存的url
PROCESSED_URLS = "processed_urls" # 已处理的url
PENDING_URLS = "pending_url" # 待处理的url
CHAPTERS = "chapter_ids" # 所有章节的名称及ID

# 应用文件目录
curr_dir = os.path.dirname(os.path.realpath(__file__))
html_dir = os.path.join(curr_dir, "html")

# URL域名
BASE_URL = "https://m10.bjzjxf.com"

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
        # if redis.exists(CACHED_URLS) and redis.sismember(CACHED_URLS, url):
        with open(filename, "r", encoding="utf8") as f:
            print("没有调用请求")
            return f.read()
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
      'Cookie': settings.COOKIE 
    }
    response = requests.get(url, headers=headers, allow_redirects=True)
    if response.history:
        for resp in response.history:
            print(resp.status_code, resp.url)
            if resp.url.find("one") != -1:
                response = requests.get(resp.url, headers=headers, allow_redirects=True)
                break
    html = response.text

    with open(filename, "w", encoding="utf8") as f:
        f.write(html)
        redis.sadd(CACHED_URLS, url)
    return html

def fetch_project():
    """
    下载章节，入口地址  https://m10.bjzjxf.com/Home/Index/index      
    所有的读取的html文件全部做缓存处理，并且把已处理跟未处理都放在redis中       
    已处理用 set 就可以，未处理用 sorted set，当作队列来用  
    还有一个缓存的 set 
    最重要的是知识点的题目内容，已处理、未处理的都是知识点

    先提取所有的章节、知识点插入数据，名字和ID存入缓存   
    每个章节的path都插入链接
    """
    url = "https://m10.bjzjxf.com/Home/Index/index"
    res = http_request(url)
    html = etree.HTML(res)
    # 所有的项目节点
    links_li = html.xpath("//div[@class='list']/ul/li/a")
    projects = [] 
    for li in links_li:
        projects.append({
            "name":  li.xpath("./span/text()")[0],
            "url":   BASE_URL + li.xpath("./@href")[0]
        })
        
    # 插入项目
    for item in projects:
        row = db.select_one("SELECT * FROM `tk_chapter` WHERE `name`=%s and pid = 0", (item["name"]))
        if row is not None:
            print("{0} 项目已存在，无法插入！".format(item["name"]))
            redis.hset(CHAPTERS, row["path"], row["id"])
            continue
        sql = "INSERT INTO `tk_chapter` ( `name`, `level`, `path` ) VALUES ( %s, %s, %s)"
        id = db.insert(sql, (item["name"], 1, item["url"]))
        redis.hset(CHAPTERS, item["url"], id)

    # 提取每个项目的章节及知识点
    for item in projects:
        project_id = redis.hget(CHAPTERS, item["url"])
        print("从redis中获取的内容", item["url"], project_id)
        fetch_chapter(item["url"], int(project_id))
    
def fetch_chapter(url, pid):
    """
    根据科目来提取章节
    :url string 科目url
    :pid 科目ID
    """
    print("项目章节提取开始：{0} {1}".format(pid, url))
    res = http_request(url)
    html = etree.HTML(res)
    # 所有的项目节点
    links_li = html.xpath("//div[@class='list']/ul/li/a")
    items = [] 
    for li in links_li:
        items.append({
            "name":  li.xpath("./span/text()")[0],
            "url":   BASE_URL + li.xpath("./@href")[0]
        })

    # 插入章节
    for item in items:
        row = db.select_one("SELECT * FROM `tk_chapter` WHERE `path`=%s", (item["url"]))
        if row is not None:
            print("{0} 章节已存在，无法插入！".format(item["name"]))
            redis.hset(CHAPTERS, row["path"], row["id"])
            continue
        sql = "INSERT INTO `tk_chapter` ( `name`, `level`, `path`, `pid` ) VALUES ( %s, %s, %s, %s)"
        data = (item["name"], 2,item["url"], pid)
        id = db.insert(sql, data)
        redis.hset(CHAPTERS, item["url"], id)

    # 根据章节来提取知识点  
    for item in items:
        chapter_id = redis.hget(CHAPTERS, item["url"])
        fetch_knows(item["url"], int(chapter_id))

def fetch_knows(url, pid):
    """
    根据章节来提取知识点
    :url string 章节url
    :pid 章节ID
    """
    print("知识点提取开始：{0} {1}".format(pid, url))
    res = http_request(url)
    html = etree.HTML(res)
    # 所有的知识点节点
    links_li = html.xpath("//div[@class='three']/ul/li/a")
    items = [] 
    for li in links_li:
        print(li.xpath('./text()'))
        print(li.xpath("./text()")[0], BASE_URL + li.xpath("./@href")[0])
        items.append({
            "name":  li.xpath("./text()")[0],
            "url":   BASE_URL + li.xpath("./@href")[0]
        })

    # 插入知识点
    for item in items:
        row = db.select_one("SELECT * FROM `tk_chapter` WHERE `name`=%s and `pid`=%s", (item["name"], pid))
        if row is not None:
            print("{0} 知识点已存在，无法插入！".format(item["name"]))
            redis.hset(CHAPTERS, row["path"], row["id"])
            continue
        sql = "INSERT INTO `tk_chapter` ( `name`, `level`, `path`, `pid` ) VALUES ( %s, %s, %s, %s)"
        data = (item["name"], 3, item["url"], pid)
        id = db.insert(sql, data)
        redis.hset(CHAPTERS, item["url"], id)
        
    # 根据知识点来提取题目
    for item in items:
        knows_id = redis.hget(CHAPTERS, item["url"])
        fetch_questions(item["url"], int(knows_id))

def fetch_questions(url, chapter_id):
    """
    根据知识点来提取题目
    :url string 知识点url
    :chapter_id 知识点ID
    """
    print("题目提取开始：{0} {1}".format(chapter_id, url))
    # 只提取 https://m10.bjzjxf.com/Home/Index/qaq/1985 这一类的题目  
    if url.find("qaq") == -1:
        print("非题目页面，跳过")
        return
    
    if redis.exists(PROCESSED_URLS) and redis.sismember(PROCESSED_URLS, url):
        print("题目已处理，跳过")
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
        answer_text = list(filter(lambda x : x != "您选择:",  answers[i].xpath("./text()"))) 

        item = {
            "title": qhtml.xpath("./div[@id={0}]/text()".format(i+1)),
            "select": "\n".join(select_list),
            "content": contents[i],
            "answer": "\n".join(answer_text),
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
    fetch_project()
    
    # fetch_questions("https://m10.bjzjxf.com/Home/Index/qaq/2568", 135 # 空白问题
    # fetch_questions("https://m10.bjzjxf.com/Home/Index/qaq/1888", 187) # html节点错乱问题
    # fetch_questions("https://m10.bjzjxf.com/Home/Index/qaq/482", 1015) # 题序提取 有多余的内容
    # fetch_questions("https://m10.bjzjxf.com/Home/Index/qaq/474", 1221) # 题干被图片替代了，选项有图就不行了
    
