#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import time
from locust import (
    HttpUser, task, between, constant,
    User, tag
) 

def my_task(user):
    user.client.get("/hello_task")

def another_task(user):
    user.client.get("/another_task")


class QuickstartUser(HttpUser):
    """
    wait_time 模拟用户执行任务的间隔时间
    client 属性是一个HttpSession的实例，可以模拟http请求，这个属性是 HttpUser所有的。   
    tasks 属性，所有的任务，由@task装饰器生成，可以指定权重，提高执行概率。 
    on_start 每个用户启动的时候都会调用此方法   
    host 属性 指定域名，命令行没有
    environment 与用户运行的环境交互
    
    $ locust # 直接运行 locustfile.py 的文件
    $ locust -f locust_files/my_locust_file.py # 指定文件名
    $ locust -f ....py --host=https://www.baidu.com # 指定域名
    $ locust -f locust_file.py WebUser MobileUser # 文件多个用户模拟类，指定两个运行    
    

    Task 负载测试启动后，用户类会创造一个线程，选取任务执行然后休眠一会儿，然后选取新任务继续。 
    通过指定tasks属性来设置任务，任务可以是 TaskSet类，或者callable，如果是函数则需要有一个参数表示用户实例
    tasks属性为数组时，随机指定一个任务。为dict时，将把值作为权重。 
    
    @tag 装饰器，标记模拟用户的任务，可以通过 `--tags` 和 `--exclude-tags` 来指定那些任务执行和不被执行 
    """
    wait_time = between(1, 2.5)  # 指定范围的随机时间
    wait_time = constant(5) # 固定值的时间
    wait_time = constant_pacing(5) # 确保任务每N秒运行一次
    
    last_wait_time = 0
    
    tasks = [my_task]
    # 以下等同于 [my_task, my_task, my_task, another_task]
    tasks = {
        my_task: 3,
        another_task: 1
    }  
    
    def wait_time(self):
        """
        创建wait_time方法，来自定义逻辑
        """
        self.last_wait_time += 1
        return self.last_wait_time
    
    @task
    def hello_world(self):
        self.client.get("/hello")
        self.client.get("/world")
        
    @task(3)
    def view_items(self):
        for item_id in range(10):
            self.client.get(f"/item?id={item_id}", name="/item") # url来分组，同样的url，通过指定name来进行分组
            time.sleep(1)
            
    def on_start(self):
        self.environment.runner.quit() # 停止任务运行   
        
    def on_stop(self):
        """
        模拟用户结束运行时调用  
        """
        pass
        

"""
指定用户weight属性设置权重，WebUser将会是MobileUser的3倍    
"""
class WebUser(User):
    weight = 3

class MobileUser(User):
    weight = 1
    

class TagUser(HttpUser):
    """
    @tag 装饰器，标记模拟用户的任务，可以通过 `--tags` 和 `--exclude-tags` 来指定那些任务执行和不被执行 
    $ locust -f ....py --tags tag1 --exclude-tags tag3
    """
    
    wait_time = constant(1)
    
    @tag('tag1')
    @task
    def task1(self):
        pass
    
    @tag('tag1', 'tag2')
    @task
    def task2(self):
        pass
    
    @tag('tag3')
    @task
    def task3(self):
        pass
    
    @task
    def task4(self):
        pass