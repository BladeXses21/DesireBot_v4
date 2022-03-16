import collections
from enum import Enum, unique

from clan_event.inventory_types.item_type import Item, EnumItemTypes


class EquippedInventory:
    def __init__(self):
        self.slots = collections.ChainMap(
            {
                EnumItemTypes.helmet: Item,
                EnumItemTypes.chest: Item,
                EnumItemTypes.pants: Item,
                EnumItemTypes.boots: Item,

                EnumItemTypes.weapon: Item
            })

    def equip(self, item: Item):
        self.slots.__setitem__(item.type, item)
