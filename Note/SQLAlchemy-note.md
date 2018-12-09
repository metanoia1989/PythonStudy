# 相关资源
- [SQLALchemy 官方文档](https://www.sqlalchemy.org/)
- [SQLAlchemy入门和进阶](https://zhuanlan.zhihu.com/p/27400862)

官方文档的脉络不太清晰，要扫过一遍并且学以致用才能感受得到。example很友好的！       

# 概览
重要的几个组件

- `Engine` 连接
- `Session` 连接池、事务，由此开始查询
- `Model` 表，类定义和表定义类似，类实例本质上是其中一行
- `Column` 列，在各个地方支持运算符操作
- `Query` 若干行，可以链式操作添加条件，查展开成SELECT，删展开成DELETE，改展开成UPDATE