#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
import scrapy
from News.items import CommentItem, PostItem, ThreadItem, Project, UserItem
from News.utils import *

class LkongSpider(scrapy.Spider):
    name = 'lkong'
    project_id = Project.LKONG
    base_url = 'http://www.lkong.net/'
    allowed_domains = ['www.lkong.net']
    start_urls = ['http://www.lkong.net/']

    def parse(self, response):
        all_a = response.css(".today+div,.todaynew+div").css("h2 a")
        all_threads = [ (x.attrib['href'], x.css('::text').get()) for x in all_a ]

        for item in all_threads:
            thread = ThreadItem()
            thread["project_id"] = self.project_id
            thread["thread_id"] = extract_url_base(item[0]).replace("forum", self.name)
            thread["thread_name"] = item[1]
            thread["thread_path"] = item[0]
            thread["thread_order"] = 100
            thread["thread_status"] = 0
            thread["thread_pid"] = 0
            yield thread

            yield scrapy.Request(item[0], callback=self.parse_thread, cb_kwargs=thread)     
            
    def parse_thread(self, response, **thread):
        """
        解析主题的帖子
        """
        # 解析当前页的帖子
        posts = response.xpath(r"//tbody[re:test(@id, 'normalthread_\d+')]")
        for item in posts:
            user = UserItem()
            user["user_id"] = "{0}-{1}".format(self.name, extract_lkong_uid(item.css(".by a::attr(href)").get())) 
            user["user_name"] = item.css(".by a::text").get()
            user["user_path"] = item.css(".by a::attr(href)").get()

            post = PostItem()
            post["thread_id"] = thread["thread_id"]
            post["user_id"] = user["user_id"]
            post["post_title"] = item.css(".new a::text").get()
            post["post_author"] = user["user_name"]
            post["post_date"] = item.css(".by em::text").get()
            post["post_path"] = item.css(".new a::attr(href)").get()
            post["post_id"] =  "{0}-{1}".format(self.name, extract_lkong_uid(item.xpath("./@id").get())) 
            post["post_order"] = 100
            
            yield user
            yield post
            
            yield scrapy.Request(post["post_path"], callback=self.parse_post, cb_kwargs=post)
        
        # 解析下一页的帖子
        next_url = response.css(".nxt::attr(href)").get()
        if next_url is not None:
            yield scrapy.Request(next_url, callback=self.parse_thread, cb_kwargs=thread)
        
    def parse_post(self, response, **post):
        """
        解析帖子
        """
        comments = response.xpath(r"//div[re:test(@id, 'post_\d+')]")
        
        for item in comments:
            contents = list(filter(lambda item: not item.isspace(), item.css(".t_f *::text").getall()))
            content = "\n".join(contents)

            comment = CommentItem()
            comment["post_id"] = post["post_id"]
            comment["comment_user"] = item.css(".authi font::text").get()
            comment["comment_content"] = content
            
            yield comment
            
        # 解析帖子的下一页
        next_url = response.css(".nxt::attr(href)").get()
        if next_url is not None:
            yield scrapy.Request(next_url, callback=self.parse_post, cb_kwargs=post)
        