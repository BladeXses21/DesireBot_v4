import json

from pydantic import BaseModel
from typing import List

from clan_event.inventory_types.item_type import Item


class Inventory(BaseModel):
    items: List[Item] = []
    max_size: int = 10

    def add_item(self, item: Item):
        if len(self.items) >= int(self.max_size):
            return

        self.items.append(item)

    def remove_item(self, item: Item):
        if len(self.items) <= 0:
            print("Inventory is empty already! Nothing to remove")
            return

        self.items.remove(item)
