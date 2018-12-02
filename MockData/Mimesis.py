#!/usr/bin/env python3
# -*- conding:utf8 -*-

from mimesis import Person
person_en = Person('en')
print(person_en.full_name())
print(person_en.age())
print(person_en.favorite_movie())
print('*' * 20)
person_zh = Person('zh')
print(person_zh.full_name())
print(person_zh.age())
print(person_zh.favorite_movie())
