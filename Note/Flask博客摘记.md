# 在Flask框架中使用jsonify和json.dumps的区别
直接用 json.dumps(data) 输出json数据，在 Content-Type 中显示的是 text/html ；即其 MIME 因为没有设置，仍然是默认的 text/html 。      
可以手动地设置 HTTP头来解决，或者直接使用 `jsonify` 
```python
return Response(json.dumps(result), 200, {'content-type':'application/json'})
```

# Flask框架扩展flask-wtf之表单处理
已安装的软件包包含一个Form类，该类必须用作用户定义表单的父级。      
WTforms包包含各种表单域的定义:

1. `TextField`	表示 `<input type ='text'>` HTML表单元素
2. `BooleanField`	表示 `<input type ='checkbox'>` HTML表单元素
3. `DecimalField`	用小数显示数字的文本字段
4. `IntegerField`	用于显示整数的文本字段
5. `RadioField`	表示`<input type ='radio'>`的HTML表单元素
6. `SelectField`	表示选择表单元素
7. `TextAreaField`	表示`<testarea>` html表单元素
8. `PasswordField`	表示`<input type ='password'>` HTML表单元素
9. `SubmitField`	表示`<input type='submit'>`表单元素

WTForms包也包含验证器类         

1. `DataRequired`	检查输入栏是否为空
2. `Email`	检查字段中的文本是否遵循电子邮件ID约定
3. `IPAddress`	验证输入字段中的IP地址
4. `Length`	验证输入字段中字符串的长度是否在给定范围内
5. `NumberRange`	在给定范围内的输入字段中验证一个数字
6. `URL`	验证输入字段中输入的URL

# Flask框架中蓝图/BluePrint详解
项目模块划分阶段，使用Blueprint(这里暂且称之为“蓝图”)。Blueprint通过把实现不同功能的module分开,从而把一个大的application分割成各自实现不同功能的module。在一个Blueprint中可以调用另一个blueprint的view function, 但要加相应的blueprint名。      
Blueprint还有其他好处，其本质上来说就是让程序更加松耦合，更加灵活，增加复用性，提高查错效率，降低出错概率。
在具体项目开发过程中，不同蓝本分别对应不同的功能模块。例如auth授权模块和项目主模块。

创建一个蓝图对象:
```python
from flask import Blueprint
admin=Blueprint('admin',__name__)
```

注册蓝图路由
```python
@admin.route('/')
def admin_index():
    return 'admin_index'
```

在应用对象上注册这个蓝图对象
```python
app.register_blueprint(admin, url_prefix='/admin')
```

蓝图的url前缀
```python
url_for('admin.index') # /admin/
```

注册静态路由        
蓝图对象创建时不会默认注册静态目录的路由。需要我们在 创建时指定 static_folder 参数。
```python
admin = Blueprint("admin",__name__,static_folder='static_admin')
admin = Blueprint("admin",__name__,static_folder='static_admin',static_url_path='/lib')
app.register_blueprint(admin,url_prefix='/admin')
```

设置模版目录    
蓝图对象默认的模板目录为系统的模版目录，可以在创建蓝图对象时使用 template_folder 关键字参数设置模板目录。
```python
admin = Blueprint('admin',__name__,template_folder='my_templates')
```

# Flask加盐密码生成generate_password_hash和验证函数check_password_hash
密码存储的主要形式:         
明文存储：肉眼就可以识别，没有任何安全性。      
加密存储：通过一定的变换形式，使得密码原文不易被识别。      

密码加密的几类方式：            
明文转码加密：BASE64, 7BIT等，这种方式只是个障眼法，不是真正的加密。        
对称算法加密：DES, RSA等。          
签名算法加密：也可以理解为单向哈希加密，比如MD5, SHA1等。加密算法固定，容易被暴力破解。如果密码相同，得到的哈希值是一样的。         
加盐哈希加密：加密时混入一段“随机”字符串（盐值）再进行哈希加密。即使密码相同，如果盐值不同，那么哈希值也是不一样的。现在网站开发中主要是运用这种加密方法。      
密码生成函数：generate_password_hash        
generate_password_hash是一个密码加盐哈希函数，生成的哈希值可通过check_password_hash()进行验证。     
```python
werkzeug.security.generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)
# 哈希之后的哈希字符串格式
method$salt$hash
```
参数说明        
password: 明文密码          
method: 哈希的方式（需要是hashlib库支持的），格式为`pbpdf2:<method>[:iterations]`。       
slat_length: 盐值的长度，默认为8        
```python
from werkzeug.security import generate_password_hash
>>> print generate_password_hash('123456')
'pbkdf2:sha1:1000$X97hPa3g$252c0cca000c3674b8ef7a2b8ecd409695aac370'
```

密码验证函数：check_password_hash           
check_password_hash函数用于验证经过generate_password_hash哈希的密码。若密码匹配，则返回真，否则返回假。         
```python
werkzeug.security.check_password_hash(pwhash, password) 
pwhash: generate_password_hash生成的哈希字符串
password: 需要验证的明文密码
```

```python
>>> from werkzeug.security import check_password_hash
>>> pwhash = 'pbkdf2:sha1:1000$X97hPa3g$252c0cca000c3674b8ef7a2b8ecd409695aac370'
>>> print check_password_hash(pwhash, '123456')
True
```