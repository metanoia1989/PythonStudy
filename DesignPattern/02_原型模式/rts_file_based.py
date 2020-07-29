#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import join

"""
这种情况下，就需要挖掘数万行代码以便找到每个类的参数值并且修改它们尤其是在开发人员必须在整个开发生命周期中数百次这样做时。
想象一下，对于一个像《星战前夜在线》这样深度依赖其 Python底层作为游戏逻辑的游戏而言，逐行查看代码会是多么糟糕的事情。
可以在一个单独的JSON文件或者一个数据库中存储这些参数，以便让游戏设计者可以在同一个位置修改单位参数为游戏设计者创建一个好用的GUI
（Graphical User Interface，图形化用户界面）
是很容易的，他们可以在这个GU上快速且轻易地进行修改，甚至不必在文本编辑器中修改这个文件。
"""
class Knight(object):
    def __init__(self, level):
        self.unit_type = "Knight"

        filename = "{}_{}.dat".format(self.unit_type, level)
        filename = join('data', filename)

        with open(filename, 'r') as parameter_file:
            lines = parameter_file.read().split("\n")
            self.life = lines[0]
            self.speed = lines[1]
            self.attack_power = lines[2]
            self.attack_range = lines[3]
            self.weapon = lines[4]

    def __str__(self):
        return "Type: {0}\n" \
            "Life: {1}\n" \
            "Speed: {2}\n" \
            "Attack Power: {3}\n" \
            "Attack Range: {4}\n" \
            "Weapon: {5}".format(
                self.unit_type,
                self.life,
                self.speed,
                self.attack_power,
                self.attack_range,
                self.weapon
            ) 

class Archer(object):
    def __init__(self, level):
        self.unit_type = "Archer"

        filename = "{}_{}.dat".format(self.unit_type, level)
        filename = join('data', filename)

        with open(filename, 'r') as parameter_file:
            lines = parameter_file.read().split("\n")
            self.life = lines[0]
            self.speed = lines[1]
            self.attack_power = lines[2]
            self.attack_range = lines[3]
            self.weapon = lines[4]

    def __str__(self):
        return "Type: {0}\n" \
            "Life: {1}\n" \
            "Speed: {2}\n" \
            "Attack Power: {3}\n" \
            "Attack Range: {4}\n" \
            "Weapon: {5}".format(
                self.unit_type,
                self.life,
                self.speed,
                self.attack_power,
                self.attack_range,
                self.weapon
            ) 

class Barracks(object):
    def build_unit(self, unit_type, level):
        if unit_type == "knight":
            return Knight(level)
        elif unit_type == "archer":
            return Archer(level)

if __name__ == "__main__":
    barracks = Barracks()
    knight1 = barracks.build_unit("knight", 1)
    archer1 = barracks.build_unit("archer", 2)
    print("[knight1] {}".format(knight1))
    print("[archer1] {}".format(archer1))