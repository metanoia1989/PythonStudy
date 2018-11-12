#!/usr/bin/env python3
# -*- conding:utf8 -*-

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try: 
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
    return None

def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn:
    :return: project id
    """
    sql = '''SELECT * FROM tasks'''
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
def select_task_by_priority(conn, priority):
    """
    Query tasks by priority
    :param conn: the Connection object
    "param priority:
    :return:
    """
    cursor = conn.cursor()
    sql = '''SELECT * FROM tasks WHERE priority=?'''
    cursor.execute(sql, (priority,))
    rows = cursor.fetchall()

    for row in rows:
        print(row)

def main():
    database = '/home/smithadam/Code/python/SQLite/sqlite.db'

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("1. Query task by priority")
        select_task_by_priority(conn, 1)

        print("2. Query all tasks")
        select_all_tasks(conn)
    
if __name__ == '__main__':
    main()
