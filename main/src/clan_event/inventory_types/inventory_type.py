import logging
from enum import Enum, unique

from clan_event.inventory_types.equipped_inventory import EquippedInventory
from clan_event.inventory_types.item_type import Item


class Inventory:
    def __init__(self):
        self.equipped = EquippedInventory()
        self.items = []
        self.max_size = 15

    def equip(self, item: Item):
        if not self.items.__contains__(item):
            print("Such item does not exist in your inventory. Therefore it cannot be equipped")
            return

        self.items.remove(item)
        self.equipped.equip(item)

    def add_item(self, item: Item):
        if len(self.items) >= self.max_size:
            return

        self.items.append(item)

    def remove_item(self, item: Item):
        if len(self.items) <= 0:
            print("Inventory is empty already! Nothing to remove")
            return

        self.items.remove(item)
