from systems.database_system import DatabaseSystem
from clan_event.lifeform_types.enemy_type import Enemy


class BossSystem(DatabaseSystem):

    def create_boss(self, name: str, health: int, attack_dmg: int, image: str):
        self.event_boss_collection.insert_one({
            'name': name,
            'health': health,
            'attack_dmg': attack_dmg,
            'image': image
        })
        return True

    def boss_fight(self, enemy: Enemy):
        self.event_battle_collection.delete_many({})

        self.event_battle_collection.insert_one({
            'name': enemy.name,
            'health': enemy.current_health,
            'attack_dmg': enemy.attack_dmg,
            'image': enemy.image
        })
        return True

    # todo костиль з курент хп треба потім пофіксити
    def get_current_boss(self):
        enemy_data = self.event_battle_collection.find_one({})
        return Enemy(enemy_data['name'], enemy_data['health'], enemy_data['health'], enemy_data['attack_dmg'],
                     enemy_data['image'])

    def get_random_boss(self):
        enemy_data = self.event_boss_collection.find_one({})
        return Enemy(enemy_data['name'], enemy_data['health'], enemy_data['health'], enemy_data['attack_dmg'],
                     enemy_data['image'])

    def change_health(self, enemy: Enemy):
        self.event_battle_collection.update_one({'name': enemy.name}, {'$set': {'health': enemy.current_health}})
        return True


boss_system = BossSystem()
