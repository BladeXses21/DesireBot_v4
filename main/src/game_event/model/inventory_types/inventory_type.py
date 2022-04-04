import json

from pydantic import BaseModel
from typing import List

from game_event.model.inventory_types.item_type import Item


class Inventory(BaseModel):
    items: List[Item] = []
    max_size: int = 10

    def add_item(self, item: Item):
        if len(self.items) >= int(self.max_size):
            return

        self.items.append(item)

    def item_by_index(self, item_index: int) -> Item | None:
        if item_index > self.items.__len__() or item_index < 1:
            return None
        return self.items.__getitem__(item_index-1)

    def remove_item(self, item_index: int):
        if len(self.items) <= 0:
            print("Inventory is empty already! Nothing to remove")
            return

        self.items.__delitem__(item_index-1)
