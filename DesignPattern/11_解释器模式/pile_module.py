#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
将特殊产品规则实现为一种内部DSL，需要为每个符号创建一个类
应用组合模式
"""

class Tab(object):
    def __init__(self, customer):
        self.items = []
        self.discounts = []
        self.customer = customer

    def calculate_cost(self):
        return sum(x.cost for x in self.items)

    def calculate_discount(self):
        return sum(x for x in self.discounts)

class Item(object):
    def __init__(self, name, item_type, cost):
        self.name = name
        self.item_type = item_type
        self.cost = cost

class ItemType(object):
    def __init__(self, name):
        self.name = name

class Customer(object):
    def __init__(self, customer_type, name):
        self.customer_type = customer_type
        self.name = name

    def is_a(self, customer_type):
        return self.customer_type == customer_type


class CustomerType(object):
    def __init__(self, customer_type):
        self.customer_type = customer_type

class Rule(object):
    def __init__(self, tab):
        self.tab = tab
        self.conditions = []
        self.discounts = []

    def add_condition(self, test_value):
        self.conditions.append(test_value)

    def add_percentage_discount(self, item_type, percent):
        if item_type == "any item":
            f = lambda x: True
        else:
            f = lambda x: x.item_type == item_type

        items_to_discount = [item for item in self.tab.items if f(item)]
        for item in items_to_discount:
            discount = Discount(item.cost * (percent / 100.0))
            self.discounts.append(discount)

    def add_discount(self, test_function, discount_function):
        discount = Discount(test_function, discount_function)
        self.discounts.add(discount)

    def apply(self):
        if all(self.conditions):
            return sum(x.amount for x in self.discounts)
        return 0


class Conditions(object):
    pass

class Condition(object):
    def __init__(self, condition_function):
        self.test = condition_function

    def evaluate(self, tab):
        return self.test(tab)

class AndCondition(object):
    def __init__(self):
        self.conditions = []

    def evaluate(self, tab):
        return all(x.evaluate(tab) for x in self.conditions)

    def add(self, condition):
        self.conditions.append(condition)

    def remove(self, condition):
        self.conditions.remove(condition)

class OrCondition(object):
    def __init__(self):
        self.conditions = []

    def evaluate(self, tab):
        return any(x.evaluate(tab) for x in self.conditions)

    def add(self, condition):
        self.conditions.append(condition)

    def remove(self, condition):
        self.conditions.remove(condition)

class Discounts(object):
    def __init__(self):
        self.children = []

    def calculate(self, tab):
        return sum(x.calculate(tab) for x in self.children)

    def add(self, child):
        self.children.append(child)

    def remove(self, child):
        self.children.remove(child)

class Discount(object):
    def __init__(self, test_function, discount_function):
        self.test = test_function
        self.discount = discount_function

    def calculate(self, tab):
        return sum(self.discount(item) for item in tab.items if self.test(item))

class TimeCondition(object):
    pass

class DayOfWeek(object):
    pass

class Time(object):
    pass

class Hour(object):
    pass

class HourTens(object):
    pass

class HourOnes(object):
    pass

class MinuteTens(object):
    pass

class MinuteOne(object):
    pass

class ItemCondition(object):
    pass

class Number(object):
    pass

class Digit(object):
    pass

class CustomerCondition(object):
    pass

if __name__ == "__main__":
    member = CustomerType("Member")
    member_customer = Customer(member, "John")
    tab = Tab(member_customer)

    pizza = ItemType("pizza")
    burger = ItemType("Burger")
    drink = ItemType("Drink")

    tab.items.append(Item("Margarita", pizza, 15))
    tab.items.append(Item("Cheddar Melt", burger, 6))
    tab.items.append(Item("Latte", drink, 4))

    rule = Rule(tab)
    rule.add_condition(tab.customer.is_a(member))
    rule.add_percentage_discount("any_item", 15)

    tab.discounts.append(rule.apply())
    print(
        "Calculated cost: {}\nDiscount applied: {}\n{} % Discount applied".format(
            tab.calculate_cost(),
            tab.calculate_discount(),
            100 * tab.calculate_discount() / tab.calculate_cost()
        )
    )
