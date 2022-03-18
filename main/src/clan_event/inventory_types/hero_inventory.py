from clan_event.inventory_types.equipped_inventory import EquippedInventory
from clan_event.inventory_types.inventory_type import Inventory
from clan_event.inventory_types.item_type import Item


class HeroInventory(Inventory):
    def __init__(self, items=[], size: int = 10,
                 equipped: EquippedInventory = EquippedInventory()):
        super().__init__(size, items)
        self.equipped = equipped

    def equip(self, item: Item):
        if not self.items.__contains__(item):
            print("Such item does not exist in your inventory. Therefore it cannot be equipped")
            return

        self.items.remove(item)
        self.equipped.equip(item)
