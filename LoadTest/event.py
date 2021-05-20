#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from locust import events
from locust.runners import MasterRunner

"""
Event 事件钩子      
test_start and test_stop 负载任务开始和结束事件 
init Locust 进程开始时触发，用于分布式模式的worker process进行初始化
所有的事件钩子参见 https://docs.locust.io/en/stable/api.html#events 
""" 


@events.test_start.add_listener
def on_test_start(enviroment, **kwargs):
    print("A new test is starting")

@events.test_stop.add_listener
def on_test_stop(enviroment, **kwargs):
    print("A new test is ending")
    
@events.init.add_listener
def on_locust_init(enviroment, **kwargs):
    if isinstance(enviroment.runner, MasterRunner):
        print("I'm on master node")
    else:
        print("I'm on worker or standlone node")
        