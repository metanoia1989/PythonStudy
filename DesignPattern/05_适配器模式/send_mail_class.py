#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
构造较大的系统，用面向对象的方式实现，比较好组织
"""

import csv
import smtplib
from email.mime.text import MIMEText

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
    with open('users.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        users = [ x for row in reader]

    mailer = Mailer()
    mailer.send(
        'me@example.com',
        [x"email" for x in users],
        "This is your message",
        "Have a good day"
    )