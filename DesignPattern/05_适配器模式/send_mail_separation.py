#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
关注点分离 Separation of Concern 
将用户信息的检索从EamilSender类中分离出来，独立维护，易于扩展
"""

class UserFetcher(object):
    """
    从csv文件中检索用户信息
    """
    def __init__(self, source):
        self.source = source

    def fetch_users():
        with open('users.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            users = [ x for row in reader]
            return users

        
class Mailer(object):
    def send(sender, recipients, subject, message):
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = [recipients]

        s = smtplib.SMTP('localhost')
        s.send_message(recipients)
        s.quit()

if __name__ == "__main__":
    user_fetcher = UserFetcher('users.csv')
    mailer = Mailer()

    mailer.send(
        'me@example.com',
        [x"email" for x in users],
        "This is your message",
        "Have a good day"
    )