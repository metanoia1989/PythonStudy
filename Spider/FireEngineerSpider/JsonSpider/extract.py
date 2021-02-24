#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import requests
import json
from pathlib import Path
import sys
from redis import StrictRedis
import re

from mysql import MySQL

# 测试MySQL
db = MySQL("localhost", "root", "root", "fire_engineer")
redis = StrictRedis()
CHAPTERS = "chapter_ids" # 所有章节的名称及ID
PAPERS = "papers_ids" # 所有试卷的ID

# URL域名

def http_request(url):
    """
    发起get请求
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'Authorization': 'Beego aHVhaGFuOmJlZWdvMjAxNQ==',
        'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxOTczNDIwIiwiZXhwIjoxNjE0NDA1MTA3LCJ1c2VySWQiOjE5NzM0MjAsImlhdCI6MTYxNDE0NTkwN30.ET3P8sy_zL0r4PvW-brICfUowQcDEMveXuRmUwA_iZCbbyHnbXpHJ5-JqP5To2QNV0gMPcBV91xlPK8Q-A1avA' 
    }
    response = requests.get(url, headers=headers, allow_redirects=True)
    return response.json()


def fetch_project():
    """
    """
    start_url = "http://wx.anzhuoxfpx.com/BeegoEduApi/api/pc/getactivemajorcourse/1973420?keywords="
    res = http_request(start_url)
        
    # 插入项目
    for item in res["data"]:
        row = db.select_one("SELECT * FROM `fire_chapter` WHERE `name`=%s and pid = 0", (item["courseName"]))
        if row is not None:
            print("{0} 项目已存在，无法插入！".format(item["courseName"]))
            redis.hset(CHAPTERS, row["name"], row["id"])
            continue
        sql = "INSERT INTO `fire_chapter` ( `name`, `level`, `path` ) VALUES ( %s, %s, %s)"
        id = db.insert(sql, (item["courseName"], 1, item["courseNo"]))
        redis.hset(CHAPTERS, item["courseName"], id)

    # # 提取每个项目的章节
    for item in res["data"]:
        project_id = redis.hget(CHAPTERS, item["courseName"])
        print("从redis中获取的内容，此章节提取开始", item["courseName"], project_id)
        fetch_chapter(item["courseId"], item["umcId"], int(project_id))

def fetch_chapter(courseId, umcId, pid):
    """
    根据科目来提取章节
    :url 科目umcID
    :pid 科目ID
    """
    chatper_base_url = "http://wx.anzhuoxfpx.com/BeegoEduApi/api/pc/getsimexamlist"
    url = "{0}/{1}/{2}/1".format(chatper_base_url, umcId, courseId)
    res = http_request(url)

    # 插入章节
    items = res["data"]["SimExamStoreList"]
    for item in items:
        row = db.select_one("SELECT * FROM `fire_chapter` WHERE `name`=%s AND `path`=%s", (item["examName"], item["simId"]))
        if row is not None:
            print("{0} 章节已存在，无法插入！".format(item["examName"]))
            redis.hset(CHAPTERS, row["name"], row["id"])
            continue
        sql = "INSERT INTO `fire_chapter` ( `name`, `level`, `path`, `pid` ) VALUES ( %s, %s, %s, %s)"
        data = (item["examName"], 2, item["simId"], pid)
        id = db.insert(sql, data)
        redis.hset(CHAPTERS, item["examName"], id)

    # 根据章节来提取知识点  
    for item in items:
        chapter_id = redis.hget(CHAPTERS, item["examName"])
        fetch_questions(courseId, umcId, item["simId"], int(chapter_id))

def fetch_questions(courseId, umcId, simId, chapter_id):
    """
    根据知识点来提取题目
    """
    print("题目提取开始：{0} {1} {2}".format(chapter_id, courseId, umcId))
    
    # 获取试卷ID    
    paper_url = "http://wx.anzhuoxfpx.com/BeegoEduApi/api/pc/gensimexamrecid"    
    paper_url = "{0}/{1}/{2}?courseId={3}".format(paper_url, umcId, simId, courseId)
    if redis.exists(PAPERS) and redis.hget(PAPERS, paper_url) is not None:
        paper_id = int(redis.hget(PAPERS, paper_url))
    else:
        paper_id = http_request(paper_url)["data"]
        redis.hset(PAPERS, paper_url, paper_id)

    questions_base_url = "http://wx.anzhuoxfpx.com/BeegoEduApi/api/pc/gensimexamreListBysrId"
    url = "{0}/{1}/{2}/-2".format(questions_base_url, umcId, paper_id)
    res = http_request(url)

    items = res["data"]["simExamExerciseListPage"]

    # 插入题目
    for i in range(len(items)):
        item = items[i]

        if isinstance(item["title"], list):
            item["title"] = item["title"].pop()
        row = db.select_one("SELECT * FROM `fire_questions` WHERE `chapter_id`=%s and `title`=%s", (chapter_id, item["title"]))
        if row is not None:
            print("{0} 题目已存在，无法插入！".format(item["title"]))
            continue
        sql = """
            INSERT INTO `fire_questions` ( `chapter_id`, `title`, `questtype`,`content`, `select`, `analyze`, `answer`, `order`) 
            VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)
        """
        order = i + 1 # 题目排序
        title = "第{0}题 【{1}】".format(i + 1, item["keyType"])
        select = [] # 选项
        options = ["a", "b", "c", "d", "e", "f", "g", "h"][0:item["optNum"]]
        for option in options:
            content = "{0} {1}".format(option.upper(), item[option])
            select.append(content)
        select = "\n".join(select)

        data = (chapter_id, title, item["keyType"], item["title"], select, item["analyze"], item["rightKey"], order)
        db.insert(sql, data)
        
    print("此知识点题目提取完毕")

    
if __name__ == "__main__":
    fetch_project()
    
    
