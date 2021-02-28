# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
import attr


class Project():
    LKONG = 1 # 龙的天空 
    PEDIY = 2 # 看雪论坛
    WUAIPOJIE = 3 # 吾爱破解 
    V2EX = 4 # v2ex
    NEWSMTH = 5 # 水木清华
    BBSPKU = 6 # 北大未名


class ThreadItem(Item):
    """
    论坛或板块分类
    """
    collection = 'thread'
    unique_fields = ['thread_id']

    project_id = Field()
    thread_id = Field()
    thread_name = Field()
    thread_path = Field()
    thread_order = Field()
    thread_status = Field()
    thread_pid = Field()

class UserItem(Item):
    """
    用户
    """
    collection = 'user'

    unique_fields = ['user_id']
    
    user_id = Field()
    user_name = Field()
    user_path = Field()

class PostItem(Item):
    """
    帖子
    """
    collection = 'post'
    
    unique_fields = ['post_id']

    user_id = Field()
    thread_id = Field()
    post_id = Field()
    post_title = Field()
    post_author = Field()
    post_date = Field()
    post_path = Field()
    post_order = Field()
    post_content = Field()
    
class CommentItem(Item):
    """
    帖子楼层
    """
    collection = 'comment'
    
    unique_fields = ['post_id', 'comment_user', 'comment_content']

    post_id = Field()
    comment_user = Field()
    comment_content = Field()