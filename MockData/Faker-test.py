#!/usr/bin/env python3
# -*- coding: utf-8  -*-

from faker import Faker, Factory
from faker.providers import internet 

fake = Faker('zh_CN')
print('## Faker 实例化对象生成虚拟数据 ##')
print('随机姓名 %s' % fake.name())
print('随机地址 %s' % fake.address())
print('随机文本 %s' % fake.text())
print('\n')

print('## Faker 工厂函数，使用providers  ##')
fake_internet = Factory.create()
fake_internet.add_provider(internet)
print('ipv4 私有地址 %s' % fake_internet.ipv4_private())

print('## Address 地址类信息 ##')
print('国家 %s' % fake.country())
print('城市 %s' % fake.city())
print('城市后缀 县、市 %s' % fake.city_suffix())
print('地址 %s' % fake.address())
print('街道 %s' % fake.street_address())
print('街道名 %s' % fake.street_name())
print('邮编 %s' % fake.postcode())
print('纬度 %s' % fake.latitude())
print('经度 %s' % fake.longitude())
print('\n')

print('## Person 人物类信息 ##')
print('姓名 %s' % fake.name())
print('姓 %s' % fake.last_name())
print('名 %s' % fake.first_name())
print('男性姓名 %s' % fake.name_male())
print('女性姓名 %s' % fake.name_female())
print('男性姓 %s' % fake.first_name_male())
print('男性名 %s' % fake.first_name_male())
print('\n')

print('## barcode 条码类信息 ##')
print('8位条码 %s' % fake.ean8())
print('13位条码 %s' % fake.ean13())
print('自定义位数条码 %s' % fake.ean(length=8))
print('\n')