#!/usr/bin/env python3
# -*- conding:utf8 -*-

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Column, Integer, Table, String
from sqlalchemy.orm import mapper,  sessionmaker

sql_uri = 'mysql+pymysql://root:kuyewen1234@127.0.0.1/sqlalchemy'
engine = create_engine(sql_uri, echo=True) # 定义引擎
metadata = MetaData(engine) # 绑定元信息

"""创建表格，初始化数据库"""
"""
users_table = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(40)),
    Column('email', String(120)))

users_table.create()
"""

"""
基本操作，插入数据
查询 删除和插入类似 都需要先实例一个 sqlalchemy.sql.dml 对
"""

"""
users_table = Table('users', metadata, autoload=True)
insert = users_table.insert()
print('插入句柄', insert)
insert.execute(name='rsj217', email='rsj217@gmail.com')
insert.execute({'name': 'ghost'}, {'name': 'test'})
"""


"""
使用ORM
使用 orm 就是 将 python class 与 数据库的 table 映射，免去直接写 sql 语句
"""
users_table = Table('users', metadata, autoload=True)
class User:
    def __repr__(self):
        return '<%s(%r, %r)>' % (self.__class__.__name__, self.name, self.email)
mapper(User, users_table) # 创建映射
user = User()
print('User实例 {}, User名字 {}'.format(user, user.name))

"""建立会话"""
Session = sessionmaker()
session = Session()
query = session.query(User)
u = query.filter_by(name='rsj217').first()
print(u)

# 插入新用户
user2 = User()
user2.name = 'new'
user2.email = 'new@gmail.com'
session.add(user2)
session.flush()
session.commit()