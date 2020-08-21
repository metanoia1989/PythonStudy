#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
设备网络 - 偏好设置
假设 personl和 person22都居住在这座房子中，并且他们具有不同的偏好，
例如起床时间、睡觉时间以及早晨或晚上应该做的事情。他们各自感觉最舒适的温度也不相同。
由于他们都是很友好的人，因此当他们都在屋里时，他们达成了折中妥协，
不过当一个或另一个人在屋里时，他们希望让系统设置为其偏好的设置。
"""

import random

class Light(object):
    """
    灯
    """
    def __init__(self, name):
        self.name = name
        self.status = self.get_status()

    def get_status(self):
        return random.choice(range(-1, 2))

    def is_online(self):
        return self.get_status() != -1

    def boot_up(self):
        self.status = 0

    def update_status(self, person_1_home, person_2_home):
        if person_1_home:
            if person_2_home:
                self.status = 1
            else:
                self.status = 0
        elif person_2_home:
            self.status = 1
        else: 
            self.status = 0

class Thermostat(object):
    """
    恒温器
    """
    def __init__(self, name):
        self.name = name
        self.status = self.get_status()

    def get_status(self):
        temp_range = [ x for x in range(-10, 31)]
        temp_range.append(None)
        return random.choice(temp_range)

    def is_online(self):
        return self.get_status() is not None

    def boot_up(self):
        pass

    def update_status(self, person_1_home, person_2_home):
        pass

class TemperatureRegulator(object):
    """
    温度调节器
    """
    def __init__(self, name):
        self.name = name
        self.status = self.get_status()

    def get_status(self):
        return random.choice(['heating', 'cooling', 'on', 'off', 'error'])

    def is_online(self):
        return self.get_status() != 'error'

    def boot_up(self):
        self.status = 'on'

    def update_status(self, person_1_home, person_2_home):
        if person_1_home:
            if person_2_home:
                self.status = 'on'
            else:
                self.status = 'heating'
        elif person_2_home:
            self.status = 'cooling'
        else: 
            self.status = 'off'


class DoorLock(object):
    """
    大门锁
    """
    def __init__(self, name):
        self.name = name
        self.status = self.get_status()
     
    def get_status(self):
        return random.choice(range(-1, 2))

    def is_online(self):
        return self.get_status() != -1

    def boot_up(self):
        pass

    def update_status(self, person_1_home, person_2_home):
        if person_1_home:
            self.status = 0
        elif person_2_home:
            self.status = 1
        else:
            self.status = 1

class CoffeeMachine(object):
    """
    咖啡机
    """
    def __init__(self, name):
        self.name = name
        self.status = self.get_status()

    def get_status(self):
        return random.choice(range(-1, 5))
        
    def is_online(self):
        return self.get_status() != -1

    def boot_up(self):
        self.status = 1

    def update_status(self, person_1_home, person_2_home):
        if person_1_home:
            if person_2_home:
                self.status = 2
            else:
                self.status = 3
        elif person_2_home:
            self.status = 4
        else: 
            self.status = 0


class Clock(object):
    """
    时钟
    """
    def __init__(self, name):
        self.name = name
        self.status = self.get_status()

    def get_status(self):
        return "{}:{}".format(random.randrange(24), random.randrange(60))

    def is_online(self):
        return True

    def boot_up(self):
        self.status = "00:00"

    def update_status(self, person_1_home, person_2_home):
        if person_1_home:
            if person_2_home:
                pass
            else:
                self.status = "00:01"
        elif person_2_home:
            self.status = "20:22"
        else: 
            pass

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