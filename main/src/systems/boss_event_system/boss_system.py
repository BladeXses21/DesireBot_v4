import random

from clan_event.model.inventory_types.enemy_inventory import EnemyInventory
from systems.database_system import DatabaseSystem
from clan_event.model.lifeform_types.enemy_type import Enemy


class BossSystem(DatabaseSystem):

    def create_boss(self, name: str, health: int, attack_dmg: int, image: str):
        self.event_boss_collection.insert_one({
            'name': name,
            'current_health': health,
            'max_health': health,
            'attack_dmg': attack_dmg,
            'image': image,
            'inventory': EnemyInventory().dict()
        })
        return True

    def get_random_boss(self):
        random_number = random.randint(0, self.event_boss_collection.count_documents({}) - 1)
        random_enemy_data = self.event_boss_collection.find().limit(-1).skip(random_number).next()
        return Enemy.parse_obj(random_enemy_data)

    def get_by_name(self, boss_name: str):
        enemy_data = self.event_boss_collection.find_one({'name': boss_name})
        return Enemy.parse_obj(enemy_data)

    def modify_inventory(self, enemy: Enemy):
        self.event_boss_collection.update_one({'name': enemy.name},
                                              {"$set": {'inventory': enemy.inventory.dict()}})
        return True


boss_system = BossSystem()
