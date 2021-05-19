#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from locust import HttpUser, between, task

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)
    
    def on_start(self):
        self.client.post("/login", {
            "username": "test_user",
            "password": ""
        })
        
    @task
    def index(self):
        self.client.get("/")
        self.client.get("/static/assert.js")
        
    @task
    def about(self):
        self.client.get("/about/")