# 相关资源
- [SQLALchemy 官方文档](https://www.sqlalchemy.org/)
- [遇到一个问题，请各位给讲解一下SQLAlchemy中的backref？](https://www.zhihu.com/question/38456789)
- [SQLalchemy relationship之lazy属性 学习笔记](https://blog.csdn.net/bestallen/article/details/52601457)
- [flask-sqlalchemy中 backref lazy的参数实例解释和选择](https://blog.csdn.net/qq_34146899/article/details/52559747)
- [Python—sqlalchemy - 详细的使用介绍](http://www.cnblogs.com/melonjiang/p/5360592.html) 需要参考
- [sqlalchemy中多对多的关系](https://blog.csdn.net/kuangshp128/article/details/61618519)

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

**列的类型**是 Column 的第一个参数:
```python
Integer	普通整数，一般是32bit
String (size)	变长字符串
Text	变长字符串，对较长或不限长度的字符做了优化
Date 日期
Boolean 布尔值
DateTime	表示为 Python datetime 对象的 时间和日期
Float	存储浮点值
Boolean	存储布尔值
PickleType	存储为一个持久化的 Python 对象
LargeBinary	存储一个任意大的二进制数据
```

**db.Column 中其余的参数指定属性的配置选项**
```python
primary_key：如果设置为True，这列就是表的主键
unique：如果设置为True，这列不允许出现重复的值
index：如果设置为True，为这列创建索引，提升查询效率
default：为这列定义默认值
comment: 字段评论
nullable: 是否为空
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

关系使用 relationship() 函数表示。然而外键必须用类 sqlalchemy.schema.ForeignKey 来单独声明          
backref 是一个在 Address 类上声明新属性的简单方法。     
lazy 决定了 SQLAlchemy 什么时候从数据库中加载数据，SQLAlchemy 会返回一个查询对象，在加载数据前您可以过滤（提取）它们。        

- `select` (默认值) 就是说 SQLAlchemy 会使用一个标准的 select 语句必要时一次加载数据。
- `joined` 告诉 SQLAlchemy 使用 JOIN 语句作为父级在同一查询中来加载关系。
- `subquery` 类似 'joined' ，但是 SQLAlchemy 会使用子查询。
- `dynamic` 在有多条数据的时候是特别有用的。不是直接加载这些数据，

如果想为反向引用(backref)定义惰性(lazy)状态，可以使用backref()函数。        
使用 backref() 函数，为反向引用（backrefs）定义惰性（lazy）状态     
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    addresses = db.relationship('Address',
        backref=db.backref('person', lazy='joined'), lazy='dynamic')
```

## db.relationship()常用的配置选项

- `backref`：在关系的另一个模型中添加反向引用
- `primaryjoin`：明确指定两个模型之间使用的联结条件。只在模棱两可的关系中需要指定
- `lazy`：决定了SQLAlchemy什么时候从数据库中加载数据。可选值有 select(首次访问时按需加载)、immediate(源对象加载后就加载)、 joined(加载记录，但使用联结)、 subquery (立即加载，但使用子查询)，noload(永不加载)和 dynamic(不加载记录，但提供加载记录的查询)
- `uselist`：如果设为Fales，表示一对一关系
- `order_by`：指定关系中记录的排序方式
- `secondary`：指定多对多关系中关系表的名字
- `secondaryjoin`：SQLAlchemy无法自行决定时，指定多对多关系中的二级联结条件


## 一对多关联          

每篇文章有一个外键指向 users 表中的主键 id， 而在 User 中使用 SQLAlchemy 提供的 relationship 描述关系。        
而用户与文章的之间的这个关系是双向的，所以我们看到上面的两张表中都定义了 relationship。     
SQLAlchemy 提供了 backref 让我们可以只需要定义一个关系          
```python
class User(Base):
      __tablename__ = 'users'
    articles = relationship('Article', backref='author', lazy='dynamic')

class Article(Base):
    __tablename__ = 'articles'
    user_id = Column(Integer, ForeignKey('users.id'))
```

db.relationship()的第一个参数表明这个关系的另一端是哪个模型。       
db.relationship()中的backref参数向address模型中添加一个person属性，从而定义反向关系。这一属性可替代person_id访问 person模型，此时获取的是模型对象，而不是外键的值。         
db.relationship()都能自行找到关系中的外键，但有时却无法决定把哪一列作为外键。例如如果address模型中有两个或以上的列定义为person模型的外键，SQLAlchemy就不知道该使用哪列。如果无法决定外键，你就要为db.relationship()提供额外参数，从而确定所用外键。 

## 一对一关系          
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

## 多对多关系         
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


## 多对多关系通俗解释          
多对多关系一个典型的例子是文章与标签之间的关系，一篇文章可以有多个标签，一个标签也可以对应多篇文章。            
把tags和posts表之间的多对多关系转换成它们各自与关联表connections之间的两个一对多关系。      
查询这个多对多关系分为两步。若想知道某篇文章有多少个标签，首先从posts和connections之间的一对多关系开始，获取这篇文章在connections表中的所有和这篇文章相关的记录，然后再按照多到一的关系在tags表中查找对应的所有标签。       
若想查找某个标签所对应的所有文章，首先从tags表和connections表之间的一对多关系开始，获取这个标签在connections表中所有的和这个标签相关的记录，然后再按照多到一的关系在posts表中查找对应的所有文章。       
多对多关系仍使用定义一对多关系的db.relationship()方法进行定义，但在多对多关系中，必须把secondary参数设为关联表。多对多关系可以在任何一个类中定义，backref参数会处理好关系的另一侧。关联表connections就是一个简单的表，不是模型，SQLAlchemy会自动接管这个表。         
```python
connections = db.Table('connections',
    db.Column('posts_id', db.Integer, db.ForeignKey('posts_id')),
    db.Column('tags_id', db.Integer, db.ForeignKey('tags_id')))
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    tags = db.relationship('Tag', secondary=connections,
        backref=db.backref('posts', lazy='dynamic'),
        lazy='dynamic')
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
```

## 多对多关系 中间表的增删改查
- [python – Flask sqlalchemy多对多插入数据](https://codeday.me/bug/20180112/117011.html)
- [flask-sqlalchemy 一对一，一对多，多对多操作](https://www.cnblogs.com/huchong/p/8797516.html)
**定义多对多关系的三个步骤**        
1. 定义一个中间表保存两个表的主键
2. 定义多对多关系的两个表的模型
3. 给每个模型都添加一个访问对方的属性注意在relationship中指定中间表

第三步的给每个模型，添加访问对方的属性，可以在一方配置 backref 即可。

**关联表的修改**        
```python
groups = session.query(Group).all()#找出所有组

h1=session.query(Host).filter(Host.name=="172.0.0.1").first()#找出h1
h2=session.query(Host).filter(Host.name=="172.0.0.2").first()#找出h2

h1.group=groups#h1关联3个组
h2.group=groups[1:-1]#h2关联两个组
```

**关联表数据的添加**
```python
p = Parent()
c = Child()
p.children.append(c)
db.session.add(p)
db.session.commit()
```

## 简单多对多中间表不采用模型的原因
- [flask-sqlalchemy 中的多对多关系里面说到中间表的建立强烈不建议使用模型，为什么？](https://www.v2ex.com/t/184723)

如果这个many-to-many关系中没有其它信息需要维护，tag和page直接引用到对方(e.g. tag.related_pages, page.related_tags)，因为不需要显示地对token做操作，也就没有必要为它创建class/model (想像这些model的下游码农不是你自己，那他应该不需要知道token table的存在)

否则，假设token记录了譬如created_at这样的额外信息，三张表的关联变成 tag <-> token <-> page，为了取得created_at就绕不开token，因此需要把token table暴露出来

## 高级多对多关系          
自引用多对多关系可在数据库中表示用户之间的关注，但却有个限制。使用多对多关系时，往往需要存储所联两个实体之间的额外信息。对用户之间的关注来说，可以存储用户关注另一个用户的日期，这样就能按照时间顺序列出所有关注者。        
这种信息只能存储在关联表中，但是在之前实现的学生和课程之间的关系中，关联表完全是由SQLAlchemy掌控的内部表。为了能在关系中处理自定义的数据，我们必须提升关联表的地位，使其变成程序可访问的模型。          
SQLAlchemy不能直接使用这个关联表，因为如果这么做程序就无法访问其中的自定义字段。相反地，要把这个多对多关系的左右两侧拆分成两个基本的一对多关系，而且要定义成标准的关系。            
```python
class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.Foreignkey('users.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    followed = db.relationship('Follow', foreign_keys=[Follow.follower_id],
        backref=db.backref('follower', lazy='joined'),
        lazy='dynamic', cascade='all, delete-orphan')
    follower = db.relationship('Follow', foreign_keys=[Follow.followed_id],
        backref=db.backref('followed', lazy='joined'),
        lazy='dynamic', cascade='all, delete-orphan')
```
cascade 参数配置在父对象上执行的操作对相关对象的影响。比如，层叠选项可设定为：将用户添加到数据库会话后，要自动把所有关系的对象都添加到会话中。层叠选项的默认值能满足大多数情况的需求，但对这个多对多关系来说却不合用。删除对象时，默认的层叠行为是把对象联接的所有相关对象的外键设为空值。但在关联表中，删除记录后正确的行为应该是把指向该记录的实体也删除，因为这样能有效销毁联接。这就是层叠选项值delete-orphan的作用。           

# SQLAlchemy模型使用
## 查询
查询的结果, 有几种不同的类型, 这个需要注意, 像是: `instance`, `instance of list`, `keyed tuple of list`, `value of list`        

### 基本查询
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

### 多表查询
```python
session.query(Blog, User).filter(Blog.user == User.id).first().User.username
session.query(Blog, User.id, User.username).filter(Blog.user == User.id).first().id
session.query(Blog.id,
              User.id,
              User.username).filter(Blog.user == User.id).first().keys()
```

### 条件查询
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

### 函数
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

# Flask-SQLAlchemy 框架配置
Flask-SQLAlchemy从Flask主配置中加载这些值。注意其中的一些在引擎创建后不能修改，所以确保尽早配置且不在运行时修改它们。           
- `SQLALCHEMY_DATABASE_URI`：用于数据库的连接，例如sqlite:////tmp/test.db
- `SQLALCHEMY_TRACK_MODIFICATIONS`：如果设置成True(默认情况)，Flask-SQLAlchemy将会追踪对象的修改并且发送信号。这需要额外的内存，如果不必要的可以禁用它。      
- `SQLALCHEMY_COMMIT_ON_TEARDOWN`：每次request自动提交db.session.commit()

常见情况下，对于只有一个Flask应用，我们需要先创建Flask应用，选择加载配置，然后创建SQLAlchemy对象时候把Flask应用传递给它作为参数。一旦创建，这个对象就包含 sqlalchemy 和 sqlalchemy.orm 中的所有函数和助手。此外它还提供一个名为 Model 的类，用于作为声明模型时的 delarative 基类。          
```python
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy
def create_app(config_name):
    #省略号部分包含了创建app等代码，请查看前面的章节
    ...
    db.init_app(app)
```

# Flask-SQLAlchemy 操作数据库
使用过滤器可以配置query对象进行更精确的数据库查询       
**常用的过滤器**

- `filter()`：把过滤器添加到原查询上，返回一个新查询
- `filter_by()`：把等值过滤器添加到原查询上，返回一个新查询
- `limit()`：使用指定的值限制原查询返回的结果数量，返回一个新查询
- `offset()`：偏移原查询返回的结果，返回一个新查询
- `order_by()`：根据指定条件对原查询结果进行排序，返回一个新查询
- `group_by()`：根据指定条件对原查询结果进行分组，返回一个新查询

**常用的执行查询方法**

- `all()`：以列表形式返回查询的所有结果
- `first()`：返回查询的第一个结果，如果没有结果，则返回 None
- `first_or_404()`：返回查询的第一个结果，如果没有结果，则终止请求，返回 404 错误响应
- `get()`：返回指定主键对应的行，如果没有对应的行，则返回 None
- `get_or_404()`：返回指定主键对应的行，如果没找到指定的主键，则终止请求，返回 404 错误响应
- `count()`：返回查询结果的数量
- `paginate()`：返回一个 Paginate 对象，它包含指定范围内的结果