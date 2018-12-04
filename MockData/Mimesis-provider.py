#!/usr/bin/env python3
# -*- conding:utf8 -*-

from mimesis import Person, Address, Business, Payment, Text, Food
from mimesis.enums import Gender

print('#'*5 + '个人信息' + '#'*5)
person = Person('zh')
# 可以传递性别给full_name()
print(person.full_name(Gender.MALE))
print(person.level_of_english())
print(person.nationality())
print(person.work_experience())
print(person.political_views())
print(person.worldview())

# 自定义名字pattern
templates = ['l-d', 'U-d']
for item in templates:
    print(person.username(template=item))

print('\n')


print('#'*5 + '地址' + '#'*5)
address = Address('zh')
print(address.coordinates())
print(address.city())
print('\n')

print('#'*5 + '地址' + '#'*5)
business = Business('zh')
print(business.company())
print(business.company_type())
print('\n')

print('#'*5 + '支付' + '#'*5)
payment = Payment('zh')
print(payment.paypal())
print(payment.credit_card_expiration_date())
print('\n')

print('#'*5 + '文字' + '#'*5)
text = Text('zh')
print(text.alphabet())
print(text.answer())
print(text.quote())
print(text.title())
print(text.word())
print(text.words())
print(text.sentence())
print('\n')

print('#'*5 + '食物' + '#'*5)
food = Food('zh')
print(food.drink())
print(food.fruit())
print(food.spices())
print('\n')