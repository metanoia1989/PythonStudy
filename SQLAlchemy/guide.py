#!/usr/bin/env python3
# -*- conding:utf8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker


engine = create_engine('mysql+pymysql://root:kuyewen1234@127.0.0.1/sqlalchemy')
ModelBase = declarative_base() # 元类

class User(ModelBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, index=True, comment='用户名')
    password = Column(String(64), nullable=False, comment='密码')
    email = Column(String(64), nullable=False, index=True, comment='邮箱')

    articles = relationship('Article', backref='author')
    userinfo = relationship('UserInfo', backref='user', uselist=False)

    def __repr__(self):
        return '<%s(%r)>' % (self.__class__.__name__, self.username)


class Article(ModelBase):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))

class UserInfo(ModelBase):
    __tablename__ = 'userinfos'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    qq = Column(String(11))
    phone = Column(String(11))
    link = Column(String(64))
    user_id = Column(Integer, ForeignKey('users.id'))

class Tag(ModelBase):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, index=True)

    def __repr__(self):
        return '<%s(%r)>' % (self.__class__.__name__, self.name)
    
article_tag = Table(
    'article_tag', ModelBase.metadata,
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('tag_id', Integer, ForeignKey('tags.id')),
)

if __name__ == '__main__':
    # ModelBase.metadata.create_all(engine)
    Sesssion = sessionmaker(bind=engine)
    session = Sesssion()
    from faker import Factory
    import random
    faker = Factory.create()

    faker_users = [User(
        username=faker.name(),
        password=faker.word(),
        email=faker.email()
    ) for i in range(10)]
    session.add_all(faker_users)

    faker_tags= [Tag(name=faker.word()) for i in range(5)]
    session.add_all(faker_tags)

    for i in range(100):
        article = Article(
            title=faker.sentence(),
            content=''.join(faker.sentences(nb=random.randint(10,20))),
            author=random.choice(faker_users),
        )
        session.add(article)
    session.commit()


