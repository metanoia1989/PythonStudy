#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import redis
import requests
import json
import re
from hashlib import md5

def main():
    # client = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)
    redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True, db=0)
    rcli = redis.StrictRedis(connection_pool=redis_pool)

    base_url = 'http://flask.pocoo.org/docs/1.0/'
    html = rcli.get('flask-index')
    if html is None:
        html = requests.get(base_url).text
        rcli.setnx('flask-index', html)


    # 链接池 
    links = rcli.hgetall('flask-links') 
    section_str = rcli.get('flask-section') 
    if section_str is not None:
        section = json.loads(section_str)
    else:
        section = None

    if links is None or section is None:
        # 提取标题和链接
        extract_match = re.search(r'id="user-s-guide".*?id="api-reference"', html, re.M|re.S)
        user_guide_html = extract_match.group()
        match = re.findall(r'href="(.*?)">(.*?)<', user_guide_html)

        section = []
        for link, title in match:
            link = base_url + link
            hash_str = md5(link.encode('utf-8')).hexdigest()
            section.append({
                "title": title,
                "url": link,
                "hash": hash_str,
            })
            rcli.hset('flask-links', hash_str, link)
        section_str = json.dumps(section)
        rcli.setnx('flask-section', section_str)

    # 页面源代码池 
    htmls = rcli.hgetall('flask-htmls') 
    if len(htmls) != len(section):
        for item in section:
            print('发起请求\n')
            key = item.get('hash')
            if rcli.hget('flask-htmls', key) is None:
                sec_html = requests.get(item.get('url')).text
                rcli.hset('flask-htmls', key, sec_html)
                htmls[key] = sec_html

if __name__ == "__main__":
    main()