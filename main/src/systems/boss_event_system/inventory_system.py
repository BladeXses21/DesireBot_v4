import random
from systems.database_system import DatabaseSystem
from clan_event.life_forms.items_type import Item


class InventorySystem(DatabaseSystem):

    def add_new_item(self, item: Item):
        self.item_collection.insert_one({
            'item_name': item.name,
            'item_type': item.item_type
        })
        return True


inventory_system = InventorySystem()
