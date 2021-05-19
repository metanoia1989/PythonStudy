#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from locust import HttpUser, TaskSet, task

class WebsiteUser(HttpUser):
    min_wait = 3000 # 执行事务之间用户等待时间的下界（单位：毫秒）
    max_wait = 6000 # 执行事务之间用户等待时间的上界（单位：毫秒）

    @task
    def baidu_index(self):
        self.client.get("/")