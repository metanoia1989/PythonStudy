#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
零售终端演示
"""

def sync_stock_items(system):
    if system == "system1":
        print("running stock sync between local and remote system1")
        print("retrieving remote  stock items from system1")
        print("updating local items")
        print('sending updates to third party system1')
    elif system == "system2":
        print("running stock sync between local and remote system2")
        print("retrieving remote  stock items from system2")
        print("updating local items")
        print('sending updates to third party system2')
    elif system == "system3":
        print("running stock sync between local and remote system3")
        print("retrieving remote  stock items from system3")
        print("updating local items")
        print('sending updates to third party system3')
    else:
        print("no volid system")

def send_transaction(transaction, system):
    if system == "system1":
        print("send transaction to system1: {0!r}".format(transaction))
    elif system == "system2":
        print("send transaction to system2: {0!r}".format(transaction))
    elif system == "system3":
        print("send transaction to system3: {0!r}".format(transaction))
    else:
        print("no volid system")


if __name__ == "__main__":
    for system in ["system1", "system2", "system3"]:
        sync_stock_items(system)
        send_transaction({
            "id": 1,
            "items": [
                {
                    "item_id": 1,
                    "amount_purchased": 3,
                    "value": 238
                }
            ]
        }, system)
        print("="*20)