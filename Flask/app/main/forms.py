#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask_wtf import Form 
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import User, Role
from flask_pagedown.fields import PageDownField

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

# 用户编辑资料表单
class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Sbumit')

# 管理员级别资料编辑表单
class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('Username', validators=[Required(), Length(1, 64), 
                        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, '
                        'numbers, dots or underscros')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Sbumit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user
    
    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Email already registered.')
    
    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already registered.')


# 文章表单
class PostForm(Form):
    title = StringField("标题", validators=[Required(), Length(1, 128)])
    body = PageDownField("内容", validators=[Required()])
    submit = SubmitField('添加')

# 评论表单
class CommentForm(Form):
    body = StringField('', validators=[Required()])
    submit = SubmitField('Submit')