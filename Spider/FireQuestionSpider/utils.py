#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from urllib.parse import urlparse

def url_to_file(url):
    """
    url转换为文件名，去除域名，后缀的斜杠转换为下划线   
    """
    path = urlparse(url).path
    path = path.lstrip("/").replace("/", "_")
    if path.find(".html") == -1:
        path += ".html"
    return path

def split_array(array, step = 2):
    return [array[i:i+step] for i in range(0, len(array), step)]