#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import radar 
import datetime

print('随机日期 %s' % radar.random_date())

print('随机日期+时间 %s' % radar.random_datetime())

print('随机时间 %s' % radar.random_time())

print('指定范围随机日期 %s' % radar.random_date(
    start=datetime.datetime(year=1985, month=1, day=1),
    stop=datetime.datetime(year=1989, month=12, day=30)
))

print('指定范围随机日期+时间 %s' % radar.random_datetime(
    start=datetime.datetime(year=1985, month=1, day=1),
    stop=datetime.datetime(year=1989, month=12, day=30)
))

print('指定范围随机时间 %s' % radar.random_time(
    start="2018-01-10T09:00:10",
    stop="2018-01-10T18:00:00",
))

# 默认使用 重量级的python-dateutil库解析日期，选择使用轻量级的radar.utils.parse(快5倍)
print('指定范围随机时间 %s' % radar.random_time(
    start="2018-01-10T09:00:10",
    stop="2018-01-10T18:00:00",
    parse=radar.utils.parse
))

# radar.utils.parse usage
start = radar.utils.parse('2018-01-01')
stop = radar.utils.parse('2018-01-05')
print('使用 radar.utils.parse 解析器 %s' % radar.random_datetime(start=start, stop=stop))