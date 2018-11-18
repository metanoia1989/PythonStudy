#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import Flask,  render_template, session, redirect, url_for, flash
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
import os.path
import os
import logging

from flask_wtf import Form 
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from flask_migrate import Migrate, MigrateCommand

from flask_mail import Mail, Message

basedir = os.path.abspath(os.path.dirname(__file__))

# 初始化
app = Flask(__name__)
app.config['SECRET_KEY'] = 'metanoia1989'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <m15171641694@163.com>'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')


db = SQLAlchemy(app)
manager = Manager(app)
Bootstrap = Bootstrap(app)
Moment = Moment(app)
migrate = Migrate(app, db)
mail = Mail(app)
logging.basicConfig(filename='./log/logger.log', level=logging.INFO)

# 集成 Python shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

# 邮件
def send_mail(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

# 表单
class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

# 模型
class Role(db.Model):
    """ Role 表模型 """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    """ User表模型 """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.name


# 路由
@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/form', methods=['GET', 'POST'])
def make_form():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            logging.info(app.config['FLASKY_ADMIN'])
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_mail(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('make_form'))
    return render_template('form.html', form=form, 
        name=session.get('name'),
        known=session.get('known', False))



if __name__ == '__main__':
    manager.run()
