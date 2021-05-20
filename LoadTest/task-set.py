#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from locust import User, TaskSet, constant

"""
将任务进行模块化
"""

class ForumSection(TaskSet):
    """
    self.user 是用户实例的引用  
    """
    wait_time = constant(1)
    
    @task(10)
    def view_thread(self):
        pass
    
    @task
    def create_thread(self):
        pass
    
    @task
    def stop(self):
        """
        TaskSet 永远不会停止执行任务，所以需要手动退出  
        中断任务
        """
        self.interrupt()
        

class LoggedInUser(User):
    wait_time = constant(5)
    tasks = { ForumSection: 2 }
    
    @task
    def my_task(self):
        pass
    
class MyUser(User):
    @task
    class MyTaskSet(TaskSet):
        pass