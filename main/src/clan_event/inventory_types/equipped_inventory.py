import collections
from enum import Enum, unique

from clan_event.inventory_types.item_type import Item, EnumItemTypes


class EquippedInventory:
    def __init__(self):
        self.slots = collections.ChainMap(
            {
                EnumItemTypes.helmet.value: None,
                EnumItemTypes.gloves.value: None,
                EnumItemTypes.chest.value: None,
                EnumItemTypes.pants.value: None,
                EnumItemTypes.boots.value: None,

                EnumItemTypes.weapon.value: None
            })

    def equip(self, item: Item):
        self.slots.__setitem__(item.type, item)
