from systems.database_system import DatabaseSystem
from clan_event.inventory_types.item_type import Item


class ItemsSystem(DatabaseSystem):

    def add_new_item(self, item: Item):
        self.item_collection.insert_one({
            'name': item.name,
            'type': item.type
        })
        return True

    def remove_item(self, item: Item):
        self.item_collection.delete_one({
            'name': item.name,
            'type': item.type
        })


items_system = ItemsSystem()
