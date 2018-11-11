#!/usr/bin/env python3
# -*- conding:utf8 -*-

def div(a, b):
    try:
        print(a/b)
    except ZeroDivisionError:
        print("Error: b should not be 0 !!")
    except Exception as e:
        print("Unexception Error: {}".format(e))
    else:
        print("Run into else only when everything goes will")
    finally: 
        print("Always run into finally block.")

# tests
div(2, 0)
div(2, 'bad type')
div(1, 2)

