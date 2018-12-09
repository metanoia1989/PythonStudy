#!/usr/bin/env python3
# -*- conding:utf8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

engine = create_engine('mysql+pymysql://root:kuyewen1234@127.0.0.1/sqlalchemy')
ModelBase = declarative_base() # 元类

class User(ModelBase):
    __tablename__ = 'auth_user'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, index=True, comment='用户名')
    password = Column(String(64), nullable=False, comment='密码')
    email = Column(String(64), nullable=False, index=True, comment='邮箱')
    articles = relationship('Article', backref='author')

    def __repr__(self):
        return '<%s(%r)>' % (self.__class__.__name__, self.username)


class Article(ModelBase):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))