#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import sqlite3

class Database:
    def __init__(self, name=None, tablename=None):
        self.conn = None
        self.cursor = None
        self.table_name = None

        if name:
            self.open(name)
        
        if tablename:
            self.tablename = tablename
        
    @property
    def tablename(self):
        return self.tablename

    @tablename.setter
    def tablename(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self.tablename = value

        
    def open(self, name):
        try:
            self.conn = sqlite3.connect(name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print("Error connecting to database!")
        
    def close(self):
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, ext_value, traceback):
        self.close()

    
    # 增删改查
    def get(self, table, columns):
        sql = "SELECT {0} from {1} LIMIT 1;".format(columns, table)
        self.cursor.execute(sql) 
        row = self.cursor.fetch()
        return row

    def gets(self, table, columns, limit=None):
        if limit:
            sql = "SELECT {0} from {1} LIMIT {2};".format(columns, table, limit)
        else:
            sql = "SELECT {0} from {1};".format(columns, table)
        self.cursor.execute(sql) 
        rows = self.cursor.fetchall()
        return rows

    def write(self, table, columns, data):
        sql = "INSERT INTO {0} ({1}) VALUES ({2});".format(table, columns, data)
        self.cursor.execute(sql)

    def delete(self, table, where):
        sql = "DELETE {0} WHERE {1};".format(table, where)
        self.cursor.execute(sql)
    
    def update(self, table, columns, data):
        sql = "UPDATE {0} SET ..."
        pass
    
    # 原生 sql
    def query(self, sql):
        self.cursor.execute(sql)