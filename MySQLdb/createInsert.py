#!/usr/bin/env python3
# -*- conding:utf8 -*-

import sys
import mysql.connector as mc

try:
    conn = mc.connect(host="192.168.1.106", user="python", passwd="python", db="python")
except mc.Error as e:
    print("Error %d: %s" % (e.args[0], e.args[1]))
    sys.exit(1)

cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS employee")
sql = """
CREATE TABLE employee (
    staff_number INTEGER PRIMARY KEY,
    fname VARCHAR(20),
);
"""