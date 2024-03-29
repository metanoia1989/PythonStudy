#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import render_template
from flask_mail import Message
from flask import current_app
from . import mail

# 邮件
def send_mail(to, subject, template, **kwargs):
    msg = Message(current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                sender=current_app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)