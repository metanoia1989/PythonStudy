#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
设备网络 - 带有启动序列
"""

import random
import unittest

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

class HomeAutomationBootTests(unittest.TestCase):
    """
    测试设备网络的启动
    """
    def setUp(self):
        self.thermostat = Thermostat("General Thermostat")
        self.thermal_regulator = TemperatureRegulator("Thermal Regulator")
        self.front_door_lock = DoorLock("Front Door Lock")
        self.coffee_machine = CoffeeMachine("Coffee Machine")
        self.bedroom_light = Light("Bedroom Light")
        self.system_clock = Clock("System Clock")

    def test_boot_thermostat_does_nothing_do_state(self):
        state_before = self.thermostat.status
        self.thermostat.boot_up()
        self.assertEqual(state_before, self.thermostat.status)

    def test_boot_thermal_regulator_turns_it_on(self):
        self.thermal_regulator.boot_up()
        self.assertEqual(self.thermal_regulator.status, 'on')


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