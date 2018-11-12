#!/usr/bin/env python3
# -*- conding:utf8 -*-

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    # """ create a database connection to a SQLite database """
    """ create a database connection to a database that resides in the memory"""
    try: 
        # conn = sqlite3.connect(db_file)
        conn = sqlite3.connect(':memory:')
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()
        
if __name__ == '__main__':
    create_connection("/home/smithadam/Code/python/SQLite/sqlite.db")
