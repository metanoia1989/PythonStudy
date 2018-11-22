#!/usr/bin/env python3
# -*- conding:utf8 -*-

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views