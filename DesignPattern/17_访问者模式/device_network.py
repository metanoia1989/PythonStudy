#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
设备网络
"""

import random

class Light(object):
    """
    灯
    """
    def __init__(self, name):
        self.name = name

    def get_status(self):
        return random.choice(range(-1, 2))

    def is_online(self):
        return self.get_status() != -1

class Thermostat(object):
    """
    恒温器
    """
    def __init__(self, name):
        self.name = name

    def get_status(self):
        temp_range = [ x for x in range(-10, 31)]
        temp_range.append(None)
        return random.choice(temp_range)

    def is_online(self):
        return self.get_status() is not None

class TemperatureRegulator(object):
    """
    温度调节器
    """
    def __init__(self, name):
        self.name = name

    def get_status(self):
        return random.choice(['heating', 'cooling', 'on', 'off', 'error'])

    def is_online(self):
        return self.get_status() != 'error'

class DoorLock(object):
    """
    大门锁
    """
    def __init__(self, name):
        self.name = name
     
    def get_status(self):
        return random.choice(range(-1, 2))

    def is_online(self):
        return self.get_status() != -1

class CoffeeMachine(object):
    """
    咖啡机
    """
    def __init__(self, name):
        self.name = name

    def get_status(self):
        return random.choice(range(-1, 5))
        
    def is_online(self):
        return self.get_status() != -1

class Clock(object):
    """
    时钟
    """
    def __init__(self, name):
        self.name = name

    def get_status(self):
        return "{}:{}".format(random.randrange(24), random.randrange(60))

    def is_online(self):
        return True

if __name__ == "__main__":
    device_network = [
        Thermostat("General Thermostat"),
        TemperatureRegulator("Thermal Regulator"),
        DoorLock("Front Door Lock"),
        CoffeeMachine("Coffee Machine"), 
        Light("Bedroom Light"),
        Light("Kitchen Light"),
        Clock("System Clock")
    ]
    for device in device_network:
        print("{} is online: \t{}".format(device.name, device.is_online()))