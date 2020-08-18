#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python3没有适用的版本非常可惜
"""

import time
import curses

if __name__ == "__main__":
    win = curses.initscr()
    curses.noecho()

    win.addstr(0, 0, "press the keys w a s d to initiate actions")
    win.addstr(1, 0, "press x to exit")
    win.addstr(2, 0, "> ")
    win.move(2, 2)

    while True:
        ch = win.getch()
        if ch is not None:
            win.move(2, 0)
            win.deleteln
            win.addstr(2, 0, "> ")
            if ch == 120:
                break
            elif ch == 97: # a
                print("Running Left")
            elif ch == 100: # d
                print("Running Right")
            elif ch == 119: # w
                print("Jumping")
            elif ch == 115: # a
                print("Crouching")
            else:
                print("Standing")
        time.sleep(0.05)
        
