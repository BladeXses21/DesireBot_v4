from systems.database_system import DatabaseSystem
from clan_event.life_forms.items_type import Item


class InventorySystem(DatabaseSystem):

    def add_new_item(self, item: Item):
        self.item_collection.insert_one({
            'item_name': item.name,
            'item_type': item.item_type
        })
        return True

    def remove_item(self, item: Item):
        self.item_collection.delete_one({
            'item_name': item.name,
            'item_type': item.item_type
        })


inventory_system = InventorySystem()
