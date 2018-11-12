#!/usr/bin/env python3
# -*- conding:utf8 -*-

import MySQLdb

conn = MySQLdb.connect(host="192.168.1.106", user="python", passwd="python", db="python")
cursor = conn.cursor()
cursor.execute("SELECT VERSION()")
row = cursor.fetchone()
print("server version: %s" % row[0])
cursor.close()
conn.close()