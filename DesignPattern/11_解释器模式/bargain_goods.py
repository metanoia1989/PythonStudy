#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
If tab contains 2 pizzas on Wednesdays cheapest on if free
Every day from 17:00 to 19:00 drinks are less 10%
All items are less 15% for members
"""
pizzas = [ item for tab.items if item.type == "pizza"]
if len(pizzas) > 2 and day_of_week == 4:
    cheapest_pizza_price = min(pizza.price for pizza in pizzas)
    tab.add_discount(cheapest_pizza_price)

drinks = [ item for tab.items if item.type == "drink" ]
if 17 < hour_now < 19:
    for item in tab.items:
        if item.type == "drink":
            item.price = item.price * 0.90

if tab.customer.is_member():
    for item in tab.items:
        item.price = item.price * 0.85
