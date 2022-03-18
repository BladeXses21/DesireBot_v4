from systems.database_system import DatabaseSystem
from clan_event.inventory_types.item_type import Item


class ItemsSystem(DatabaseSystem):

    def create_new_item(self, item: Item):
        self.item_collection.insert_one({
            'name': item.name,
            'type': item.type
        })
        return True

    def find_by_name(self, item_name: str):
        item_data = self.item_collection.find_one({'name': item_name})
        if item_data is None:
            return

        return Item(item_data['name'], item_data['type'])

    def remove_item(self, item: Item):
        self.item_collection.delete_one({
            'name': item.name,
            'type': item.type
        })


items_system = ItemsSystem()
