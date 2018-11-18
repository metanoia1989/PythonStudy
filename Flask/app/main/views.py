#!/usr/bin/env python3
# -*- conding:utf8 -*-

from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import NameForm
from ..models import User

@main.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@main.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@main.route('/form', methods=['GET', 'POST'])
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
        return redirect(url_for('.make_form'))
    return render_template('form.html', form=form, 
        name=session.get('name'),
        known=session.get('known', False))