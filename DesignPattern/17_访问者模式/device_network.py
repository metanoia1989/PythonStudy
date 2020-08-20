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
    def __init__(self):
        pass

    def get_status(self):
        return random.choice(range(-1, 2))

class Thermostat(object):
    """
    恒温器
    """
    def __init__(self):
        pass 

    def get_status(self):
        temp_range = [ x for x in range(-10, 31)]
        temp_range.append(None)
        return random.choice(temp_range)

class TemperatureRegulator(object):
    """
    温度调节器
    """
    def __init__(self):
        pass 

    def get_status(self):
        return random.choice(['heating', 'cooling', 'on', 'off', 'error'])

class DoorLock(object):
    """
    大门锁
    """
    def __init__(self):
        pass 
     
    def get_status(self):
        return random.choice(range(-1, 2))

class CoffeeMachine(object):
    """
    咖啡机
    """
    def __init__(self):
        pass 

    def get_status(self):
        return random.choice(range(-1, 5))
        

class Clock(object):
    """
    时钟
    """
    def __init__(self):
        pass 

    def get_status(self):
        return "{}:{}".format(random.randrange(24), random.randrange(60))

if __name__ == "__main__":
    device_network = [
        Thermostat(),
        TemperatureRegulator(),
        DoorLock(),
        CoffeeMachine(), 
        Light(),
        Light(),
        Clock()
    ]
    for device in device_network:
        print(device.get_status())