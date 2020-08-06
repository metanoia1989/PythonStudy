#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
为一个社交网络媒体库创建一个适配器
"""

import csv
import smtplib
from email.mime.text import MIMEText

class Mailer(object):
    def send(self, sender, recipients, subject, message):
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = [recipients]

        s = smtplib.SMTP('localhost')
        s.send_message(recipients)
        s.quit()

class Logger(object):
    def output(self, message):
        print("{Logger}".format(message))

class LoggerAdapter(object):
    def __init__(self, what_i_have):
        self.what_i_have = what_i_have

    def send(self, sender, recipients, subject, message):
        log_message = "From: {}\nTo: {}\nSubject: {}\nMessage: {}".format(
            sender,
            recipients,
            subject,
            message
        )
        self.what_i_have.output(log_message)

    def __getattr__(self, attr):
        return getattr(self.what_i_have, attr) 

class UserFetcher(object):
    """
    从csv文件中检索用户信息
    """
    def __init__(self, source):
        self.source = source

    def fetch_users(self):
        with open('users.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            users = [ x for row in reader]
            return users

if __name__ == "__main__":
    user_feacher = UserFetcher("users.csv")
    
    mailer = Mailer()

    mailer.send(
        'me@example.com',
        [x["email"] for x in users],
        "This is your message",
        "Have a good day"
    )