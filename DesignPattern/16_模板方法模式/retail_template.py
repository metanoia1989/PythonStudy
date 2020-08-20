#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
零售终端的模板方法模式
的确让代码清晰很多很多
"""

from abc import ABCMeta, abstractmethod

class ThirdPartyInteractionTemplate(metaclass=ABCMeta):
    def sync_stock_items(self):
        self._sync_stock_items_step_1()
        self._sync_stock_items_step_2()
        self._sync_stock_items_step_3()
        self._sync_stock_items_step_4()

    def send_transaction(self, transaction):
        self._send_transaction(transaction)

    @abstractmethod
    def _send_transaction(self):
        pass

    @abstractmethod
    def _sync_stock_items_step_1(self):
        pass

    @abstractmethod
    def _sync_stock_items_step_2(self):
        pass

    @abstractmethod
    def _sync_stock_items_step_3(self):
        pass

    @abstractmethod
    def _sync_stock_items_step_4(self):
        pass

class System1(ThirdPartyInteractionTemplate):
    def _send_transaction(self, transaction):
        print("send transaction to system1: {0!r}".format(transaction))

    def _sync_stock_items_step_1(self):
        print("running stock sync between local and remote system1")

    def _sync_stock_items_step_2(self):
        print("retrieving remote  stock items from system1")

    def _sync_stock_items_step_3(self):
        print("updating local items")

    def _sync_stock_items_step_4(self):
        print('sending updates to third party system1')

class System2(ThirdPartyInteractionTemplate):
    def _send_transaction(self, transaction):
        print("send transaction to system2: {0!r}".format(transaction))

    def _sync_stock_items_step_1(self):
        print("running stock sync between local and remote system2")

    def _sync_stock_items_step_2(self):
        print("retrieving remote  stock items from system2")

    def _sync_stock_items_step_3(self):
        print("updating local items")

    def _sync_stock_items_step_4(self):
        print('sending updates to third party system2')

class System3(ThirdPartyInteractionTemplate):
    def _send_transaction(self, transaction):
        print("send transaction to system3: {0!r}".format(transaction))

    def _sync_stock_items_step_1(self):
        print("running stock sync between local and remote system3")

    def _sync_stock_items_step_2(self):
        print("retrieving remote  stock items from system3")

    def _sync_stock_items_step_3(self):
        print("updating local items")

    def _sync_stock_items_step_4(self):
        print('sending updates to third party system3')

if __name__ == "__main__":
    transaction = {
        "id": 1,
        "items": [
            {
                "item_id": 1,
                "amount_purchased": 3,
                "value": 238
            }
        ]
    }

    for C in [System1, System2, System3]:
        print("=" * 30)
        system = C()
        system.sync_stock_items()
        system.send_transaction(transaction)