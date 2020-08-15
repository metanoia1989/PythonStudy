#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
用函数作为命令
"""
def text_writer(string1, string2):
    print("Writing {} - {}".format(string1, string2))

class Invoker(object):
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def run(self):
        for command in self.commands:
            command["function"](*command["params"])

if __name__ == "__main__":
    invoker = Invoker()
    invoker.add_command({
        "function": text_writer,

        "params": ( "Command 1", "String 1" )
    })
    invoker.add_command({
        "function": text_writer,
        "params": ( "Command 2", "String 2" )
    })
    invoker.run()