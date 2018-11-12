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

def update_task(conn, task):
    """
    update priority, begin_date, and end_date of a week
    :param conn:
    :param task:
    :return: project id
    """
    sql = '''UPDATE `tasks` 
            SET priority = ?,
                begin_date = ?,
                end_date = ?
            WHERE id = ?'''
    cursor = conn.cursor()
    cursor.execute(sql, task)

def main():
    database = '/home/smithadam/Code/python/SQLite/sqlite.db'

    # create a database connection
    conn = create_connection(database)
    with conn:
        update_task(conn, (2, '2015-01-04', '2015-01-06', 2))
    
if __name__ == '__main__':
    main()
