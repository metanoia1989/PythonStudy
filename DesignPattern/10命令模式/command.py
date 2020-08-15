#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单的命令模式实现
运行时动态创建新的行为，在后续的某个时间再执行。        
将命令串联在一起，就能够考虑撤销所执行的命令。  
"""
class Command(object):
    def __init__(self, receiver, text):
        self.receiver = receiver
        self.text = text

    def execute(self):
        self.receiver.print_message(self.text)

class Receiver(object):
    def print_message(self, text):
        print("Message received: {}".format(text))

class Invoker(object):
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def run(self):
        for command in self.commands:
            command.execute()

if __name__ == "__main__":
    receiver = Receiver()

    command1 = Command(receiver, "Execute Command 1")
    command2 = Command(receiver, "Execute Command 2")

    invoker = Invoker()
    invoker.add_command(command1)
    invoker.add_command(command2)
    invoker.run()