#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
工具类
"""

import re

def extract_url_base(url):
    """
    提取URL的base部分，排除后缀
    """
    left = url.rfind("/") + 1
    right = url.rfind(".")
    return url[left:right]

def extract_lkong_uid(url):
    """
    提取龙空的uid
    """
    match = re.search("(\d+)", url)
    if match is None:
        return None
    return match.group(0)
    


def test_thread_to_tid():
    url = "http://www.lkong.net/forum-8-1.html" 
    id = extract_url_base(url)
    assert(id == "forum-8-1")

def test_extract_lkong_uid():
    url = "http://www.lkong.net/home.php?mod=space&uid=1222823"
    id = extract_lkong_uid(url)
    assert(id == "1222823")

if __name__ == "__main__":
    test_thread_to_tid()
    test_extract_lkong_uid() 