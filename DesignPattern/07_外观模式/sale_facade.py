#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Inovice(object):
    def __init__(self, customer):
        pass

class Customer(object):
    def __init__(self, customer_id):
        pass

class Item(object):
    def __init__(self, item_barcode):
        pass

class InvoiceLine(object):
    def __init__(self, item):
        pass

class Receipt(object):
    def __init__(self, invoice, payment_type):
        pass

class LoyaltyAccount(object):
    def __init__(self):
        pass


class Sale(object):
    def __init__(self):
        pass

    @staticmethod
    def make_customer():
        return Customer()

    @staticmethod
    def make_item(item_barcode):
        return Item(item_barcode)

    @staticmethod
    def make_invoice_line(item):
        return InvoiceLine(item)

    @staticmethod
    def make_receipt(invoice, payment_type):
        return Receipt(invoice, payment_type)

    @staticmethod
    def maek_loyalty_account(customer):
        return LoyaltyAccount(customer)

    @staticmethod
    def fetch_invoice(inovice_id):
        return Inovice(customer)

    @staticmethod
    def fetch_customer(customer_id):
        return Customer(customer_id)

    @staticmethod
    def fetch_item(item_barcode):
        return Item(item_barcode)

    @staticmethod
    def fetch_invoice_line(line_item_id):
        return InvoiceLine(item)

    @staticmethod
    def fetch_receipts(invoice_id):
        return Receipt(invoice, payment_type)

    @staticmethod
    def fetch_loyalty_account(customer_id):
        return LoyaltyAccount(customer)

    @staticmethod
    def add_item(invoice, item_barcode, amount_purchased):
        item = Item.fetch(item_barcode)
        item.amount_in_stock = amount_purchased
        item.save()
        invoice_line = InvoiceLine.make(item)
        invoice.add_line(invoice_line)

    @staticmethod
    def finalize(invoice):
        invoice.calculate() 
        invoice.save()

        loyalt_account = LoyaltyAccount.fetch(invoice.customer)
        loyalt_account.calculate(invoice)
        loyalt_account.save()

    @staticmethod
    def generate_receipt(invoice, payment_type):
        receipt = Receipt(invoice, payment_type)
        receipt.save()

def nice_sales_processor(customer_id, item_dict_list, payment_type):
    invoice = Sale.make_invoice(customer_id)

    for item_dict in item_dict_list:
        Sale.add_item(invoice, item_dict["barcode"], item_dict_list["amount_purchased"])

    Sale.finalize(invoice)
    Sale.generate_receipt(invoice, payment_type)