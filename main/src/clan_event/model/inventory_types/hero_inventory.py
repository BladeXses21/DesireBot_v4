from clan_event.model.inventory_types.equipped_inventory import EquippedInventory
from clan_event.model.inventory_types.inventory_type import Inventory
from clan_event.model.inventory_types.item_type import Item


class HeroInventory(Inventory):
    equipped: EquippedInventory = EquippedInventory()

    def equip(self, item: Item):
        if not self.items.__contains__(item):
            print("Such item does not exist in your inventory. Therefore it cannot be equipped")
            return

        self.items.remove(item)
        previous_item = self.equipped.equip(item)

        if previous_item is not None:
            self.items.append(previous_item)
