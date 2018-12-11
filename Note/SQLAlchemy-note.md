# 相关资源
- [SQLALchemy 官方文档](https://www.sqlalchemy.org/)
- [遇到一个问题，请各位给讲解一下SQLAlchemy中的backref？](https://www.zhihu.com/question/38456789)
- [SQLalchemy relationship之lazy属性 学习笔记](https://blog.csdn.net/bestallen/article/details/52601457)
- [flask-sqlalchemy中 backref lazy的参数实例解释和选择](https://blog.csdn.net/qq_34146899/article/details/52559747)

官方文档的脉络不太清晰，要扫过一遍并且学以致用才能感受得到。example很友好的！       

# 概览
重要的几个组件

- `Engine` 连接
- `Session` 连接池、事务，由此开始查询
- `Model` 表，类定义和表定义类似，类实例本质上是其中一行
- `Column` 列，在各个地方支持运算符操作
- `Query` 若干行，可以链式操作添加条件，查展开成SELECT，删展开成DELETE，改展开成UPDATE

# 连接URI的格式
SQLAlchemy 把一个引擎的源表示为一个连同设定引擎选项的可选字符串参数的 URI
```python
dialect+driver://username:password@host:port/database
postgresql://scott:tiger@localhost/mydatabase
mysql://scott:tiger@localhost/mydatabase
sqlite:////absolute/path/to/foo.db
```


# 创建模型
用 Column 来定义一列。列名就是您赋值给那个变量的名称。如果您想要在表中使用不同的名称，您可以提供一个想要的列名的字符串作为可选第一个参数。主键用 primary_key=True 标记。可以把多个键标记为主键，此时它们作为复合主键。      

列的类型是 Column 的第一个参数:
```python
Integer	一个整数
String (size)	有长度限制的字符串
Text	一些较长的 unicode 文本
DateTime	表示为 Python datetime 对象的 时间和日期
Float	存储浮点值
Boolean	存储布尔值
PickleType	存储为一个持久化的 Python 对象
LargeBinary	存储一个任意大的二进制数据
```



```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

engine = create_engine('mysql+mysqldb://root@localhost:3306/blog?charset=utf8')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, index=True)
    password = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False, index=True)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.username)
```

在 User 类中，用 `__tablename__` 指定在 MySQL 中表的名字。      
类中的每一个 Column 代表数据库中的一列，在 Colunm中，指定该列的一些配置。       
第一个字段代表类的数据类型， String, Integer, Text, Boolean, SmallInteger, DateTime     
nullable=False 代表这一列不可以为空         
index=True 表示在该列创建索引           
定义 `__repr__`，在交互shell中，打印模型类，将会自动调用这个方法。      


# 模型关联
## relationship
从lazy参数的不同值所执行的sql语句出发，结合one-to-many和many-to-many的关系，分析lazy参数取不同值(dynamic, joined, select)在不同场景下的选择

**一对多关联**          
关系使用 relationship() 函数表示。然而外键必须用类 sqlalchemy.schema.ForeignKey 来单独声明          
backref 是一个在 Address 类上声明新属性的简单方法。     
lazy 决定了 SQLAlchemy 什么时候从数据库中加载数据，SQLAlchemy 会返回一个查询对象，在加载数据前您可以过滤（提取）它们。        

- `select` (默认值) 就是说 SQLAlchemy 会使用一个标准的 select 语句必要时一次加载数据。
- `joined` 告诉 SQLAlchemy 使用 JOIN 语句作为父级在同一查询中来加载关系。
- `subquery` 类似 'joined' ，但是 SQLAlchemy 会使用子查询。
- `dynamic` 在有多条数据的时候是特别有用的。不是直接加载这些数据，

使用 backref() 函数，为反向引用（backrefs）定义惰性（lazy）状态     
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    addresses = db.relationship('Address',
        backref=db.backref('person', lazy='joined'), lazy='dynamic')
```



每篇文章有一个外键指向 users 表中的主键 id， 而在 User 中使用 SQLAlchemy 提供的 relationship 描述关系。        
而用户与文章的之间的这个关系是双向的，所以我们看到上面的两张表中都定义了 relationship。     
SQLAlchemy 提供了 backref 让我们可以只需要定义一个关系          
```python
class User(Base):
      __tablename__ = 'users'
    articles = relationship('Article', backref='author')

class Article(Base):
    __tablename__ = 'articles'
    user_id = Column(Integer, ForeignKey('users.id'))
```

**一对一关系**          
在 User 中我们只定义了几个必须的字段， 但通常用户还有很多其他信息，但这些信息可能不是必须填写的，我们可以把它们放到另一张 UserInfo 表中，这样User 和 UserInfo 就形成了一对一的关系。        
一对一关系是基于一对多定义，定义方法和一对多相同，只是需要添加 userlist=False 。        
```python
class User(Base):
    __tablename__ = 'users'
    userinfo = relationship('UserInfo', backref='user', uselist=False)

class UserInfo(Base):
    __tablename__ = 'userinfos'
    user_id = Column(Integer, ForeignKey('users.id'))
```

**多对多关系**          
一遍博客通常有一个分类，好几个标签。标签与博客之间就是一个多对多的关系。多对多关系不能直接定义，需要分解成俩个一对多的关系，为此，需要一张额外的表来协助完成。
```python
tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('page_id', db.Integer, db.ForeignKey('page.id'))
)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.relationship('Tag', secondary=tags,
        backref=db.backref('pages', lazy='dynamic'))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
```

映射到数据: `Base.metadata.create_all(engine)`

# SQLAlchemy模型使用
## 查询
查询的结果, 有几种不同的类型, 这个需要注意, 像是: `instance`, `instance of list`, `keyed tuple of list`, `value of list`        

**基本查询**
```python
session.query(User).filter_by(username='abc').all()
session.query(User).filter(User.username=='abc').all()
session.query(Blog).filter(Blog.create >= 0).all()
session.query(Blog).filter(Blog.create >= 0).first()
session.query(Blog).filter(Blog.create >= 0 | Blog.title == 'A').first()
session.query(Blog).filter(Blog.create >= 0 & Blog.title == 'A').first()
session.query(Blog).filter(Blog.create >= 0).offset(1).limit(1).scalar()
session.query(User).filter(User.username ==  'abc').scalar()
session.query(User.id).filter(User.username ==  'abc').scalar()
session.query(Blog.id).filter(Blog.create >= 0).all()
session.query(Blog.id).filter(Blog.create >= 0).all()[0].id
dict(session.query(Blog.id, Blog.title).filter(Blog.create >= 0).all())
session.query(Blog.id, Blog.title).filter(Blog.create >= 0).first().title
session.query(User.id).order_by('id desc').all()
session.query(User.id).order_by('id').first()
session.query(User.id).order_by(User.id).first()
session.query(User.id).order_by(-User.id).first()
session.query('id', 'username').select_from(User).all()
session.query(User).get('16e19a64d5874c308421e1a835b01c69')
```

**多表查询**
```python
session.query(Blog, User).filter(Blog.user == User.id).first().User.username
session.query(Blog, User.id, User.username).filter(Blog.user == User.id).first().id
session.query(Blog.id,
              User.id,
              User.username).filter(Blog.user == User.id).first().keys()
```

**条件查询**
```python
from sqlalchemy import or_, not_
session.query(User).filter(or_(User.id == '',
                               User.id == '16e19a64d5874c308421e1a835b01c69')).all()
session.query(User).filter(not_(User.id == '16e19a64d5874c308421e1a835b01c69')).all()
session.query(User).filter(User.id.in_(['16e19a64d5874c308421e1a835b01c69'])).all()
session.query(User).filter(User.id.like('16e19a%')).all()
session.query(User).filter(User.id.startswith('16e19a')).all()
dir(User.id)
```

**函数**
```python
from sqlalchemy import func
session.query(func.count('1')).select_from(User).scalar()
session.query(func.count('1'), func.max(User.username)).select_from(User).first()
session.query(func.count('1')).select_from(User).scalar()
session.query(func.md5(User.username)).select_from(User).all()
session.query(func.current_timestamp()).scalar()
session.query(User).count()
```

## 更新
```python
# 通过update方式
session.query(User).filter(User.username == 'abc').update({'name': '123'})
session.commit()

# 通过修改模型实例属性值
user = session.query(User).filter_by(username='abc').scalar()
user.name = '223'
session.commit()
```

如果涉及对属性原值的引用, 则要考虑 `synchronize_session` 这个参数.      

- `'evaluate'` 默认值, 会同时修改当前 session 中的对象属性.
- `'fetch'` 修改前, 会先通过 select 查询条目的值.
- `False` 不修改当前 session 中的对象属性.

在默认情况下, 因为会有修改当前会话中的对象属性, 所以如果语句中有 SQL 函数, 或者"原值引用", 那是无法完成的操作, 自然也会报错。   
这种情况下, 就不能要求 SQLAlchemy 修改当前 session 的对象属性了, 而是直接进行数据库的交互, 不管当前会话值。
```python
# 对属性原值引用 - 报错
from sqlalchemy import func
session.query(User).update({User.name: func.trim('123 ')})
session.query(User).update({User.name: User.name + 'x'})

# 使用 synchrozie_session
session.query(User).update({User.name: User.name + 'x'}, synchronize_session=False)
```
是否修改当前会话的对象属性, 涉及到当前会话的状态. 如果当前会话过期, 那么在获取相关对象的属性值时, SQLAlchemy 会自动作一次数据库查询, 以便获取正确的值。     
执行了 update 之后, 虽然相关对象的实际的属性值已变更, 但是当前会话中的对象属性值并没有改变. 直到 session.commit() 之后, 当前会话变成"过期"状态, 再次获取 user.name 时, SQLAlchemy 通过 user 的 id 属性, 重新去数据库查询了新值. (如果 user 的 id 变了呢? 那就会出事了啊.)           
synchronize_session 设置成 'fetch' 不会有这样的问题, 因为在做 update 时已经修改了当前会话中的对象了.        
不管 synchronize_session 的行为如何, commit 之后 session 都会过期, 再次获取相关对象值时, 都会重新作一次查询.            
## 删除
```python
session.query(User).filter_by(username='abc').delete()
user = session.query(User).filter_by(username='abc').first()
session.delete(user)
```
删除同样有像修改一样的 synchronize_session 参数的问题, 影响当前会话的状态.

## JOIN 联表
```python
r = session.query(Blog, User).join(User, Blog.user == User.id).all()
for blog, user in r:
    print blog.id, blog.user, user.id

r = session.query(Blog, User.name, User.username).join(User, Blog.user == User.id).all()
print r
```

## 只查一列
用query的with_entites方法，查询返回的不再是DeclarativeMeta对象，而是单纯的tuple对象         
如果有外键关系，可以使用join进行关联，join的参数要用relationship的backref值             
```python
User.query.with_entities(User.id,User.dept_id).all()
User.query.with_entities(User.id,User.username,Department.department_name).join(User.dept).all()
```
