#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
观察者模式的任务处理
"""

class Task(object):
    def __init__(self, user, _type):
        self.user = user
        self._type = _type
        self.observers = set()

    def register(self, observer):
        self.observers.add(observer)

    def unregister(self, observer):
        self.observers.discard(observer)

    def unregister_all(self):
        self.observers = set()

    def update_all(self):
        for observer in self.observers:
            observer.update(self)

        
class User(object):
    def __init__(self, wallet):
        self.wallet = wallet
        self.badges = []
        self.experience = 0

    def add_experience(self, amount):
        self.experience += amount

    def update(self, observed):
        self.add_experience(1)

    def __str__(self):
        return "Wallet\t{}\nExperience\t{}\n+ Badges +\n{}\n+++++++++++++".format(
            self.wallet,
            self.experience,
            "\n".join([ str(x) for x in self.badges ])
        )

class Wallet(object):
    def __init__(self):
        self.amount = 0

    def increase_balance(self, amount):
        self.amount += amount

    def decrease_balance(self, amount):
        self.amount -= amount

    def update(self, observed):
        self.increase_balance(5)

    def __str__(self):
        return str(self.amount)

class Badge(object):
    def __init__(self, name, _type):
        self.points = 0
        self.name = name
        self._type = _type
        self.awarded = False

    def add_points(self, amount):
        self.points += amount

        if self.points > 3:
            self.awarded = True

    def update(self, observed):
        if task._type == self._type:
            self.add_points(2)

    def __str__(self):
        if self.awarded:
            award_string = "Earned"
        else:
            award_string = "Unearned"

        return "{}: {} [{}]".format(
            self.name,
            award_string,
            self.points
        )

if __name__ == "__main__":
    wallet = Wallet()
    user = User(wallet)

    user.badges.append(Badge("Fun Badge", 1))
    user.badges.append(Badge("Bravery Badge", 2))
    user.badges.append(Badge("Missing Badge", 3))

    tasks = [Task(user, 1), Task(user, 1), Task(user, 3)]
    for task in tasks:
        task.register(wallet)
        task.register(user)
        for badge in user.badges:
            task.register(badge)

    for task in tasks:
        task.update_all()

    print(user)