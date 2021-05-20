#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from locust import HttpUser, TaskSet, task, between
from json import JSONDecodeError

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def request_type(self):
        """
        支持 get post put 等请求方式 
        """
        response = self.client.post("/login", { "username": "testuser", "password": "secret" })
        print("Response status code: ", response.status_code)
        print("Response text: ", response.text)
        response = self.client.get("/my-profile")
        
    @task    
    def response_validate(self):
        with self.client.get("/", catch_response=True) as response:
            if response.text != "Success":
                response.failure("Got wrong response") 
            elif response.elapsed.total_seconds() > 0.5:
                response.failure("Request took too long")
                
        
        with self.client.get("/does_not_exist", catch_response=True) as response:
            if response.status_code = 404:
                response.success()
                
    @task
    def json_decode(self):
        with self.client.post("/", json={"foo": 43, "bar": None}, catch_response=True) as response:
            try:
                if response.json()["gretting"] != "hello":
                    response.failure("Did not get excepted value in greeting")
            except JSONDecodeError:
                response.failure("Response could not be decoded as JSON")
            except KeyError:
                response.failure("Response did not contain expceted key greeting")
                
    @task
    def group_request(self):
        """
        动态请求URL归为一组
        这些请求的信息将会归组为 /blog/?id[id]
        """
        for i in range(10):
            self.client.get("/blog?id=%1" % 1, name="/blog?id=[id]")
            