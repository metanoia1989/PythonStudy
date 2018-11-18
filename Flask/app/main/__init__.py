#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors