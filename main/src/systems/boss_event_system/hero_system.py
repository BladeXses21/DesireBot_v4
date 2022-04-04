import time
from collections import namedtuple
from types import SimpleNamespace

from discord import User

from config import NEW_HERO_START_ATTACK, NEW_HERO_START_HEALTH, HERO_REGEN
from game_event.model.lifeform_types.hero_type import Hero
from systems.database_system import DatabaseSystem


class HeroSystem(DatabaseSystem):
    def create_new_hero(self, user: User) -> Hero:
        hero = Hero(id=user.id, name=user.name, current_health=NEW_HERO_START_HEALTH,
                    max_health=NEW_HERO_START_HEALTH, attack_dmg=NEW_HERO_START_ATTACK)

        self.game_hero_collection.insert_one({
            'id': hero.id,
            'name': hero.name,
            'current_health': self.health_to_time(hero.current_health, hero.max_health),
            'max_health': hero.max_health,
            'attack_dmg': hero.attack_dmg,
            'inventory': hero.inventory.dict(),
            'respawn_time': hero.respawn_time
        })
        return hero

    def get_hero_by_user(self, user: User):
        hero_data = self.game_hero_collection.find_one({'id': user.id}, {})

        # if user exist return him
        if hero_data is not None:
            hero_data['current_health'] = self.time_to_health(hero_data['current_health'], hero_data['max_health'])
            return Hero.parse_obj(hero_data)

        new_hero = hero_system.create_new_hero(user)
        return new_hero

    def get_hero_by_id(self, id: int):
        hero_data = self.game_hero_collection.find_one({'id': id}, {})

        # if user exist return him
        if hero_data is not None:
            hero_data['current_health'] = self.time_to_health(hero_data['current_health'], hero_data['max_health'])
            return Hero.parse_obj(hero_data)

        print(f"Hero with id = {id} doesnt exist ")
        return None

    def name_by_id(self, user_id: int) -> str:
        return self.game_hero_collection.find_one({'id': user_id}, {'name': 1})['name']

    def health_change(self, hero: Hero):
        self.game_hero_collection.update_one({'id': hero.id},
                                             {"$set": {'current_health': self.health_to_time(hero.current_health
                                                                                              , hero.max_health),
                                                        'respawn_time': hero.respawn_time}
                                               })
        return True

    def modify_inventory(self, hero: Hero):
        self.game_hero_collection.update_one({'id': hero.id},
                                             {"$set": {'inventory': hero.inventory.dict()}})
        return True

    @staticmethod
    def time_to_health(time_millis: int, max_health: int) -> int:
        now = time.time()
        difference = (time_millis - now)

        if difference <= 0:
            return max_health
        return max_health - int(difference / HERO_REGEN)

    @staticmethod
    def health_to_time(current_health: int, max_health: int) -> int:
        now = time.time()

        missing_health = max_health - current_health

        seconds_to_regen = now + (missing_health * HERO_REGEN)

        return int(seconds_to_regen)


hero_system = HeroSystem()
