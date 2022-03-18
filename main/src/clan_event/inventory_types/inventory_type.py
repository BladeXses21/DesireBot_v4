import json
from clan_event.inventory_types.item_type import Item


class Inventory:
    def __init__(self, size: int = 10, items=[]):
        self.items = items
        self.max_size = size

    def add_item(self, item: Item):
        if len(self.items) >= int(self.max_size):
            return

        self.items.append(item)

    def remove_item(self, item: Item):
        if len(self.items) <= 0:
            print("Inventory is empty already! Nothing to remove")
            return

        self.items.remove(item)

    def to_dict(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))
