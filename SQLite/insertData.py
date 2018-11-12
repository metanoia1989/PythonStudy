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

def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = '''INSERT INTO `projects`(name, begin_date, end_date)
            VALUES(?,?,?)'''
    cursor = conn.cursor()
    cursor.execute(sql, project)
    return cursor.lastrowid

def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
    sql = '''INSERT INTO `tasks`(name, priority, status_id, project_id, begin_date, end_date)
            VALUES(?,?,?,?,?,?)'''
    cursor = conn.cursor()
    cursor.execute(sql, task)
    return cursor.lastrowid

def main():
    database = '/home/smithadam/Code/python/SQLite/sqlite.db'

    # create a database connection
    conn = create_connection(database)
    with conn:
        # create a new project
        project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30')
        project_id = create_project(conn, project)

        # tasks
        task1 = ('Analyze the requirements of the app', 1, 1, project_id, '2015-01-01', '2015-01-02')
        task2 = ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')

        # create tasks
        create_task(conn, task1)
        create_task(conn, task2)
    
if __name__ == '__main__':
    main()
