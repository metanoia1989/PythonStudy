#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
from pathlib import Path
import sys
import json
import re

from docx import Document
import xlwt

from mysql import MySQL
import settings
from utils import *

# 测试MySQL
db = MySQL(settings.DATABASE_HOST, settings.DATABASE_USERNAME, settings.DATABASE_PASSWORD, settings.DATABASE_NAME)

# 应用文件目录
curr_dir = os.path.dirname(os.path.realpath(__file__))
excel_dir = os.path.join(curr_dir, "excel")

def init_env():
    """ 
    初始化环境
    """ 
    # 创建缓存目录
    if not os.path.exists(excel_dir):
        os.mkdir(excel_dir)
    os.chdir(excel_dir)
    
def export_base_project(project_id):
    """ 
    导出单个项目为 word
    """ 
    # 查询项目名称
    sql = "SELECT name from `tk_chapter` WHERE id = %s"
    project_name = db.select_one(sql, (project_id))["name"]
    
    # 查询项目的章节
    sql = "SELECT id, name from `tk_chapter` WHERE pid = %s"
    chapters = db.select_all(sql, (project_id))
    
    # 查询章节对应的知识点
    for i, item in enumerate(chapters):
        sql = "SELECT id, name from `tk_chapter` WHERE pid = %s"
        knows = db.select_all(sql, (item["id"]))
        
        # 查询知识点对应的题目
        for j, know in enumerate(knows):
            sql = "SELECT `id`, `title`,`content`,`select`,`answer` from `tk_questions` WHERE chapter_id = %s"
            questions = db.select_all(sql, (know["id"]))
            knows[j]["questions"] = questions

        chapters[i]["child"] = knows
        
    excel = xlwt.Workbook()
    sheet = excel.add_sheet("Sheet1")
    headers = [
        "序号",	"考题标题", "考题科目", "考题科目", "考题类型", "考题答案", 	
        "选项1", "选项2", "选项3",  "选项4", "选项5", "图片", "解析", "关键词"
    ]
    # 写标题行
    row_header = sheet.row(0)
    for i in range(len(headers)):
        row_header.write(i, headers[i]) 
        

    number = 1 # 序号
    for chapter in chapters:
        for know in chapter["child"]: 
            for question in know["questions"]:
                row = sheet.row(number)

                # 提取题目类型
                question_type = re.findall(r"\((.+)\)", question["title"])[0]
                # 提取答案和解析
                try:
                    [ answer, analyze ] = re.findall(r"^正确答案:([A-D]+)[\s\S]*?\(单击隐藏\)(.*)$", question["answer"], re.DOTALL|re.UNICODE)[0]
                except IndexError:
                    answer = ""
                    analyze = re.findall(r"\(单击隐藏\)([\s\S]*)$", question["answer"], re.DOTALL|re.UNICODE)[0].strip()
                    

                selects = question["select"].split("\n")
                selects = list(map(lambda select: re.sub("^[A-F] ", "", select), selects))
                if len(selects) < 5:
                    selects += [ "" for x in range(0, 5 - len(selects))]

                item = [
                    number,
                    question["content"], # 考题标题
                    chapter["name"], # 章节
                    know["name"], # 知识点
                    question_type, # 考题类型 
                    answer, # 考题答案
                    *selects, # 5个选项
                    "", # 图片
                    analyze, # 解析
                    "", # 关键词
                ]
                for cell in range(len(item)):
                    row.write(cell, item[cell])
                
                number += 1
        
    filename = project_name.strip().replace("/", " ") + ".xlsx"
    excel.save(filename)


def export_middle_project(project_id):
    """
    导出初级及中级的知识点
    """
    # 查询项目名称
    sql = "SELECT name from `tk_chapter` WHERE id = %s"
    project_name = db.select_one(sql, (project_id))["name"]
    
    # 查询项目的章节
    sql = "SELECT id, name from `tk_chapter` WHERE pid = %s"
    chapters = db.select_all(sql, (project_id))
    
    # 查询章节对应的知识点
    for i, item in enumerate(chapters):
        sql = "SELECT id, name from `tk_chapter` WHERE pid = %s"
        knows = db.select_all(sql, (item["id"]))
        
        # 查询知识点对应的题目
        for j, know in enumerate(knows):
            sql = "SELECT `id`, `title`,`content`,`select`,`answer` from `tk_questions` WHERE chapter_id = %s"
            questions = db.select_all(sql, (know["id"]))
            knows[j]["questions"] = questions

        chapters[i]["child"] = knows
        
    excel = xlwt.Workbook()
    sheet = excel.add_sheet("Sheet1")
    headers = [
        "序号",	"考题标题", "考题科目", "考题科目", "考题科目" "考题类型", "考题答案", 	
        "选项1", "选项2", "选项3",  "选项4", "选项5", "图片", "解析", "关键词"
    ]
    # 写标题行
    row_header = sheet.row(0)
    for i in range(len(headers)):
        row_header.write(i, headers[i]) 

    number = 1 # 序号
    for chapter in chapters:
        for know in chapter["child"]: 
            # 知识点名称分割提取为知识点及单元，检测是否有培训单元，有就提取，否则留空
            if know["name"].find("培训单元") != -1:
                [ know_name, unit_name] = re.findall(r"^(.*)(培训单元.*)$", know["name"], re.DOTALL|re.UNICODE)[0]
            else:
                know_name = know["name"]
                unit_name = ""

            for question in know["questions"]:
                row = sheet.row(number)

                # 提取题目类型
                question_type = re.findall(r"\((.+)\)", question["title"])[0]
                # 提取答案和解析
                try:
                    [ answer, analyze ] = re.findall(r"^正确答案:([A-D]+)[\s\S]*?\(单击隐藏\)(.*)$", question["answer"], re.DOTALL|re.UNICODE)[0]
                except IndexError:
                    answer = ""
                    analyze = re.findall(r"\(单击隐藏\)([\s\S]*)$", question["answer"], re.DOTALL|re.UNICODE)[0].strip()
                    
                selects = question["select"].split("\n")
                selects = list(map(lambda select: re.sub("^[A-F] ", "", select), selects))
                if len(selects) < 5:
                    selects += [ "" for x in range(0, 5 - len(selects))]

                item = [
                    number,
                    question["content"], # 考题标题
                    chapter["name"], # 章节
                    know_name, # 知识点
                    unit_name, # 单元
                    question_type, # 考题类型 
                    answer, # 考题答案
                    *selects, # 5个选项
                    "", # 图片
                    analyze, # 解析
                    "", # 关键词
                ]
                for cell in range(len(item)):
                    row.write(cell, item[cell])
                
                number += 1
        
    filename = project_name.strip().replace("/", " ") + ".xlsx"
    excel.save(filename)


def export_all():
    """
    只导出以下模板，基础知识用 章节-知识点 这样的模板
    初级、中级使用 章节-知识点-单元 这样的模板
    3	新版《基础知识》所有科目必考 
    4	新初级 消防设施操作员 练习题/视频 
    5	新中级(操作方向) 练习题/视频 
    6	新中级(维保方向) 练习题/视频
    """

    # 导出 基础知识 科目
    export_base_project(3)

    # 导出 初级 中级 科目
    for i in [4, 5, 6]:
        export_middle_project(i)

    # 导出 高级
    for i in [7, 8]:
        export_middle_project(i)


        
def write_excel_test():
    """
    写入excel文件测试
    """
    # 创建 xls 文件对象 
    wb = xlwt.Workbook()
    
    # 新增工作表
    sheet1 = wb.add_sheet("成绩")
    sheet2 = wb.add_sheet("汇总")
    
    # 按照位置来添加数据，第一个参数是行，第二个参数是列
    sheet1.write(0, 0, "姓名")
    sheet1.write(0, 1, "专业")
    sheet1.write(0, 2, "科目")
    sheet1.write(0, 3, "成绩")

    sheet1.write(1, 0, "张三")
    sheet1.write(1, 1, "信息与通信工程")
    sheet1.write(1, 2, "数值分析")
    sheet1.write(1, 3, 88)

    sheet1.write(2, 0, "李四")
    sheet1.write(2, 1, "物联网工程")
    sheet1.write(2, 2, "数字信号处理分析")
    sheet1.write(2, 3, 95)

    sheet1.write(3, 0, "王华")
    sheet1.write(3, 1, "电子与通信工程")
    sheet1.write(3, 2, "模糊数学")
    sheet1.write(3, 3, 90)
    
    # 写第二个sheet
    sheet2.write(0, 0, "总分")
    sheet2.write(1, 0, 273)
    wb.save("text.xlsx")
    
if __name__ == "__main__":
    init_env()
    
    export_all()
    # write_excel_test()
    