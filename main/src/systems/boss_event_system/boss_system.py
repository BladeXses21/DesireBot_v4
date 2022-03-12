from systems.database_system import DatabaseSystem
from clan_event.life_forms.enemy_type import Enemy


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
        self.event_battle_collection.insert_one({
            'name': enemy.name,
            'health': enemy.health,
            'attack_dmg': enemy.attack_dmg,
            'image': enemy.image
        })
        return True

    def get_current_boss(self):
        get_enemy = self.event_battle_collection.find_one({})
        return Enemy(get_enemy['name'], get_enemy['health'], get_enemy['attack_dmg'], get_enemy['image'])

    def get_random_boss(self):
        get_enemy = self.event_boss_collection.find_one({})
        return Enemy(get_enemy['name'], get_enemy['health'], get_enemy['attack_dmg'], get_enemy['image'])

    def change_health(self, enemy: Enemy):
        self.event_battle_collection.update_one({'name': enemy.name}, {'$set' : {'health': enemy.health}})
        return True


boss_system = BossSystem()
