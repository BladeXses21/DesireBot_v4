import random

from game_event.model.inventory_types.inventory_type import Inventory


class EnemyInventory(Inventory):

    def random_item(self):
        return self.items.__getitem__(random.randint(0, self.items.__len__()-1))
