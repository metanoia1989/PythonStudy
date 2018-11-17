#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import request, Flask, make_response, redirect, abort, render_template
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent

@app.route('/yangzhu')
def section():
    return render_template('index.html')

@app.route('/400')
def bad():
    return '<h1>Bad Request</h1>', 400

@app.route('/res')
def res():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response

@app.route('/redirect')
def gorun():
    return redirect('http://www.runoob.com', 302)

@app.route('/user/<id>')
def get_user(id):
    user = { 'name': 'smithadam'}
    if not user:
        abort(404)
    return '<h1>Hello, %s</h1>' % user['name']

if __name__ == '__main__':
    manager.run()
