#!/usr/bin/env python3
# -*- conding:utf8 -*-

from __future__ import unicode_literals, absolute_import
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

ModelBase = declarative_base() # 元类

class User(ModelBase):
    __tablename__ = 'auth_user'

    id = Column(Integer, primary_key=True)
    date_joined = Column(DateTime, comment='时间戳')
    username = Column(String(length=30), comment='用户名')
    password = Column(String(length=128), comment='密码')


with get_session() 