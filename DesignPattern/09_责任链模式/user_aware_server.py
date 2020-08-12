#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

class User(object):
    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email

    @classmethod
    def get_verified_user(cls, username, password):
        return User(
            username,
            password,
            "{}@demo.com".format(username)
        )

def application(env, start_response):
    authorization_header = env["HTTP_AUTHORIZATION"]
    header_array = authorization_header.split()
    encoded_string = header_array[1]
    decoded_string = base64.b64decode(encoded_string).decode('utf-8')
    username, password = decoded_string.split(':')

    user = User.get_verified_user(username, password)

    start_response('200 OK', [('Content-Type', 'text/html')])

    path = env["PATH_INFO"].split("/")
    if "goodbye" in path:
        response = "Goodbye {}!".format(user.name)
    else:
        response = "Hello {}!".format(user.name)

    return [response.encode('utf-8')]
