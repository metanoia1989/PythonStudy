#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
复杂的pos交易处理
"""

import datetime
import random

class Invoice(object):
    def __init__(self, customer):
        self.timestamp = datetime.datetime.now()
        self.number = self.generate_number()
        self.lines = []
        self.total = 0
        self.tax = 0
        self.customer = customer

    def save(self):
        """
        保存发票信息以一定的顺序到存储中
        """
        pass

    def send_to_printer(self):
        pass

    def add_line(self, invoice_line):
        self.lines.append(invoice_line) 
        self.calculate()

    def remove_line(self, line_item):
        try:
            self.lines.remove(line_item)
        except ValueError as e:
            print("could not remove {} because there is no such item in the invoice".format(line_item))

    def calculate(self):
        self.total = sum(x.total * x.amount for x in self.lines)
        self.tax = sum(x.total * x.tax_rate for x in self.lines)

    def generate_number(self):
        rand = random.randint(1, 1000)
        return "{} {}".format(self.timestamp, rand)

class InvoiceLine(object):
    def __init__(self, line_item):
        pass

    def save(self):
        pass

class Receipt(object):
    def __init__(self, invoice, payment_type):
        self.invoice = invoice
        self.customer = invoice.customer
        self.payment_type = payment_type
        
    def save(self):
        pass

class Item(object):
    def __init__(self):
        pass

    @classmethod
    def fetch(cls, item_barcode):
        pass

    def save(self):
        pass

class Customer(object):
    def __init__(self):
        pass

    @classmethod
    def fetch(cls, customer_code):
        pass

    def save(self):
        pass 

class LoyaltyAccount(object):
    def __init__(self):
        pass

    @classmethod
    def fetch(cls, customer):
        pass

    def calculate(self, invoice):
        pass

    def save(self):
        pass

def complex_sales_processor(customer_code, item_dict_list, payment_type):
    customer = Customer.fetch_customer(customer_code)
    invoice = Invoice()

    for item_dict in item_dict_list:
        item = Item.fetch(item_dict["barcode"])
        item.amount_in_sock - item_dict["amount_purchased"]
        item.save()
        invoice_line = InvoiceLine(item)
        invoice.add_line(invoice_line)

    invoice.calculate()
    invoice.save()
    loyalt_account = LoyaltyAccount.fetch(customer)
    loyalt_account.calculate(invoice)
    loyalt_account.save()

    receipt = Receipt(invoice, payment_type)
    receipt.save()