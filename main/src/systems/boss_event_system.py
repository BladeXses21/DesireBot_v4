from clan_event.user_type import User
from systems.database_system import DatabaseSystem
from clan_event.boss_type import Enemy
import random


class EventSystem(DatabaseSystem):

    def create_boss(self, name: str, health: int, atack_dmg: int, image: str):
        self.event_boss_collection.insert_one({
            'name': name,
            'health': health,
            'atack_dmg': atack_dmg,
            'image': image
        })
        return True

    def boss_fight(self, enemy: Enemy):
        self.battle_collection.insert_one({
            'name': enemy.name,
            'health': enemy.health,
            'atack_dmg': enemy.atack_dmg,
            'image': enemy.image
        })
        return True

    def get_current_boss(self):
        get_enemy = self.battle_collection.find_one({})
        return Enemy(get_enemy['name'], get_enemy['health'], get_enemy['atack_dmg'], get_enemy['image'])

    def get_random_boss(self):
        get_enemy = self.event_boss_collection.find_one({})
        return Enemy(get_enemy['name'], get_enemy['health'], get_enemy['atack_dmg'], get_enemy['image'])

    def change_health_current_boss(self, enemy: Enemy):
        self.battle_collection.update_one({}, {"$set": {'health': enemy.health}})
        return True

    def get_user_who_atack(self, member_id: int):
        get_user = self.clan_member_details_collection.find_one({'member_id': member_id}, {})
        return User(get_user['member_name'], get_user['member_health'], get_user['member_id'], get_user['member_dmg'])


event_system = EventSystem()