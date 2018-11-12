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

def delete_task(conn, id):
    """
    Delete a task by task id
    :param conn:
    :param id: id of the task
    :return:
    """
    sql = '''DELETE FROM `tasks` WHERE id=?'''
    cursor = conn.cursor()
    cursor.execute(sql, (id,))

def delete_all_task(conn):
    """
    Delete all rows in the tasks table
    :param conn:
    :return:
    """
    sql = '''DELETE FROM `tasks`'''
    cursor = conn.cursor()
    cursor.execute(sql)

def main():
    database = '/home/smithadam/Code/python/SQLite/sqlite.db'

    # create a database connection
    conn = create_connection(database)
    with conn:
        delete_task(conn, 2)
        # delete_all_task(conn)
    
if __name__ == '__main__':
    main()
