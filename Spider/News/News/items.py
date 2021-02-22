# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import attr


class Proejct():
    LKONG = 1 # 龙的天空 
    PEDIY = 2 # 看雪论坛
    WUAIPOJIE = 3 # 吾爱破解 
    V2EX = 4 # v2ex
    NEWSMTH = 5 # 水木清华
    BBSPKU = 6 # 北大未名


@attr.s
class ThreadItem():
    """
    论坛或板块分类
    """
    collection = 'thread'
    
    project_id = attr.s()
    thread_name = attr.s()
    thread_path = attr.s()
    thread_order = attr.s(init=100)
    thread_status = attr.s(init=1)
    thread_pid = attr.s(init=0)

@attr.s
class UserItem():
    """
    用户
    """
    collection = 'user'
    
    user_name = attr.s()

@attr.s
class PostItem():
    """
    帖子
    """
    collection = 'post'
    
    thread_id = attr.s()
    user_id = attr.s()
    post_title = attr.s()
    post_author = attr.s()
    post_date = attr.s()
    post_path = attr.s()
    post_order = attr.s(init=100)