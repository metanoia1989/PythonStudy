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


# 创建模型
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