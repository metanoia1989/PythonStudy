#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
pos刷卡简略封装模式
"""

class Inovice(object):
    def __init__(self, customer):
        pass

class Customer(object):
    def __init__(self, customer_id):
        pass

class Item(object):
    def __init__(self, item_barcode):
        pass

class Facade(object):
    @staticmethod
    def make_invoice(customer):
        return Invoice(customer)

    @staticmethod
    def make_customer(customer_id):
        return Customer(customer_id)

    @staticmethod
    def make_item(item_barcode):
        return Item(item_barcode)