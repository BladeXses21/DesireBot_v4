import random

from clan_event.inventory_types.enemy_inventory import EnemyInventory
from systems.database_system import DatabaseSystem
from clan_event.lifeform_types.enemy_type import Enemy


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

    def boss_fight(self, enemy: Enemy):
        self.event_battle_collection.delete_many({})

        self.event_battle_collection.insert_one({
            'name': enemy.name,
            'current_health': enemy.current_health,
            'max_health': enemy.max_health,
            'attack_dmg': enemy.attack_dmg,
            'image': enemy.image,
            'inventory': enemy.inventory.dict()
        })
        return True

    def get_current_boss(self):
        enemy_data = self.event_battle_collection.find_one({})
        return Enemy.parse_obj(enemy_data)

    def get_random_boss(self):
        random_number = random.randint(0, self.event_boss_collection.count_documents({}) - 1)
        random_enemy_data = self.event_boss_collection.find().limit(-1).skip(random_number).next()
        return Enemy.parse_obj(random_enemy_data)

    def get_by_name(self, boss_name: str):
        enemy_data = self.event_boss_collection.find_one({'name': boss_name})
        return Enemy.parse_obj(enemy_data)

    def change_health(self, enemy: Enemy):
        self.event_battle_collection.update_one({'name': enemy.name},
                                                {'$set': {'current_health': enemy.current_health}})
        return True

    def modify_inventory(self, enemy: Enemy):
        self.event_hero_collection.update_one({'name': enemy.name},
                                              {"$set": {'inventory': enemy.inventory.dict()}})
        return True


boss_system = BossSystem()
