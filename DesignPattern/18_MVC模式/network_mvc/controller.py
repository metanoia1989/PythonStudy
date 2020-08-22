#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from model import NameModel, TimeModel
from view import GreetingView

class GreetingController(object):
    def __init__(self):
        self.name_model = NameModel()
        self.time_model = TimeModel()

        self.view = GreetingView()

    def handle(self, request):
        if request in self.name_model.get_name_list():
            self.view.generate_greeting(
                name=request, 
                time_of_day=self.time_model.get_time_of_day(),
                known=True
                )
        else:
            self.name_model.save_name(request)
            self.view.generate_greeting(
                name=request, 
                time_of_day=self.time_model.get_time_of_day(),
                known=False
                )

if __name__ == "__main__":
    request_handler = GreetingController()
    request_handler.handle(sys.argv[1])