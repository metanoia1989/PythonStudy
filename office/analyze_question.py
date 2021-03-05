#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
分析 word 内容，提取题目、选项
"""

import os
import sys
import docx
import re
import json

curr_dir = os.path.dirname(os.path.realpath(__file__))
docx_file = os.path.join(curr_dir, "测试试卷.docx")

def extract_type(text):
    """
    从字符串中提取出单选题、多选题、判断题的字样
    """
    regex = "(单选题|多选题|判断题)"
    return re.search(regex, text).group(0)
    
def extract_decide(text):
    """
    提取判断题
    """
    regex = "(√|×)"
    result = re.search(regex, text)
    if result is None:
        return (None, None)
    answer = result.group(0)
    text = re.sub(regex, "", text)
    text = re.sub("^\s?\d+\.\s?", "", text).rstrip()
    return (text, answer)
    
def extract_choice(text):
    """
    提取选择题
    """
    # regex = "(（\s?)([A-Z]+)(\s?）)"
    # regex = "(（\s?)([A-Z]+)(\s?）)"
    regex = "([（|\(]\s?)([A-Z]+)(\s?[）|\)])"
    result = re.search(regex, text)
    if result is None:
        return (None, None)
    answer = result.group(2)
    text = re.sub(regex, r"\1\3", text)
    text = re.sub("^\s?\d+\.\s?", "", text).rstrip()
    return (text, answer)

def isMultipleSelector(text):
    """
    文本是否包含多个选项
    """
    regex = r"(A|B|C|D|E|F|G|H)\s+\w+"
    results = re.findall(regex, text) 
    if len(results) > 3:
        return True

    regex = r"(A|B|C|D|E|F|G|H)\s?[\u4e00-\u9fa5]+"
    results = re.findall(regex, text) 
    return len(results) > 3
    
def extractMultipleSelector(text):
    regex = r"[A|B|C|D|E|F|G|H]\s\w+"
    results = re.findall(regex, text) 
    if len(results) > 3:
        return results

    regex = "[A|B|C|D|E|F|G|H]\s?[\u4e00-\u9fa5]+"
    results = re.findall(regex, text)
    return results
    

def analyze_document():
    doc = docx.Document(docx_file)
    boxs = {
        "单选题": [],
        "多选题": [],
        "判断题": [],
    }
    types = ["单选题", "多选题", "判断题"]
    
    questype = ""
    selectorStart = False # 是否开始提取选项
    selector = []
    item = None
    for paragraph in doc.paragraphs:
        # 提取题目类型 
        styleName = paragraph.style.name     
        if styleName == "Heading 2":
            type = extract_type(paragraph.text) 
            if type in types:
                questype = type

        text = paragraph.text 
        if styleName != "Normal" or questype == "" or text == "":
            continue

        question = answer = None

        if questype == "判断题":
            [ question, answer ] = extract_decide(text)
            if question is None or answer is None:
                continue

            item = {
                "question": question,
                "answer": answer,
            }
            boxs[questype].append(item)
            continue

        # 提取单选题
        if questype == "单选题" or questype == "多选题":
            if selectorStart: # 提取选项
                # 一行包含多个选项，直接完成一道题目的提取
                if isMultipleSelector(text):
                    item["selector"] = extractMultipleSelector(text)
                    boxs[questype].append(item)
                    # 重置状态
                    selectorStart = False
                    item = None
                    selector = []
                    continue
                else:
                    selector.append(text.strip())
                    
            else: # 提取题目表述
                if len(selector) > 2 and selectorStart: # 上一道题选项提取完毕
                    boxs[questype].append(item)
                    # 重置状态
                    selectorStart = False
                    item = None
                    selector = []
                    
                [ question, answer ] = extract_choice(text)
                if question is not None or answer is not None:
                    item = {
                        "question": question,
                        "answer": answer,
                    }
                    selector = [] # 重置选项
                    selectorStart = True # 进行选项提取


            
    with open(curr_dir + "/result.json", "w", encoding="utf8") as f:
        json.dump(boxs, f, indent=4, ensure_ascii=False)


def test_extract_type():
    texts = [
        "一、单选题（20*1分）",
        "二、多选题",
        "   判断题 "
    ]
    results = ["单选题", "多选题", "判断题"]
    for t in texts:
        assert(extract_type(t) in results)
        
def text_extract_decide():
    texts = [
        "10.每种型号的红外测温仪都有自己特定的测温范围。（ √ ）",
        "3.“防”和“消”是不可分割的整体，“消”是“防”的先决条件，“消”必须与“防”紧密结合，“防”与“消”是实现消防安全的两种必要手段，两者互相联系，互相渗透，相辅相成，缺一不可。（ × ）",
        "24."
    ]
    
    for t in texts:
        result = extract_decide(t)
        print(result)
        
def text_is_multiple_selector():
    texts = [
        "A安全第一  B减少火灾危害   C生命至上   D以人为本",
        "A设置防火卷帘或防火幕等简易防火分隔物的上部	",
        "A SS50  B SS65  C SS100  D SS150",
        "A 200  B 50  C 150  D 100",
    ] 
    for t in texts:
        result = isMultipleSelector(t)
        print(result)
        print(extractMultipleSelector(t))

    print(extract_choice("职业需具备的特征有（  ABCDE   ）"))


def test_main():
    # test_extract_type()
    # text_extract_decide()
    text_is_multiple_selector()


if __name__ == "__main__":
    test_main()
    
    analyze_document()