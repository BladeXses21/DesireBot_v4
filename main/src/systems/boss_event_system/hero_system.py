import time
import json
from collections import namedtuple
from types import SimpleNamespace

from discord import User

from clan_event.inventory_types.equipped_inventory import EquippedInventory
from clan_event.inventory_types.hero_inventory import HeroInventory
from clan_event.inventory_types.inventory_type import Inventory
from clan_event.inventory_types.item_type import Item, EnumItemTypes
from config import NEW_HERO_START_ATTACK, NEW_HERO_START_HEALTH
from clan_event.lifeform_types.hero_type import Hero
from systems.database_system import DatabaseSystem


class HeroSystem(DatabaseSystem):
    def create_new_hero(self, user: User) -> Hero:
        hero = Hero(id=user.id, name=user.name, current_health=NEW_HERO_START_HEALTH,
                    max_health=NEW_HERO_START_HEALTH, attack_dmg=NEW_HERO_START_ATTACK)

        self.event_hero_collection.insert_one({
            'id': hero.get_id(),
            'name': hero.name,
            'current_health': self.health_to_time(hero.current_health, hero.max_health),
            'max_health': hero.max_health,
            'attack_dmg': hero.attack_dmg,
            'inventory': hero.inventory.dict()
        })
        return hero

    def get_hero_by_user(self, user: User):
        hero_data = self.event_hero_collection.find_one({'id': user.id}, {})

        # if user exist return him
        if hero_data is not None:
            hero_data['current_health'] = self.time_to_health(hero_data['current_health'], hero_data['max_health'])
            return Hero.parse_obj(hero_data)

        new_hero = hero_system.create_new_hero(user)
        return new_hero

    def name_by_id(self, user_id: int) -> str:
        return self.event_hero_collection.find_one({'id': user_id}, {'name': 1})['name']

    def health_change(self, hero: Hero):
        self.event_hero_collection.update_one({'id': hero.get_id()},
                                              {"$set": {'current_health': self.health_to_time(hero.current_health
                                                                                              , hero.max_health)}})
        return True

    def modify_inventory(self, hero: Hero):
        self.event_hero_collection.update_one({'id': hero.get_id()},
                                              {"$set": {'inventory': hero.inventory.dict()}})
        return True

    @staticmethod
    def time_to_health(time_millis: int, max_health: int) -> int:
        now = time.time()
        difference = (time_millis - now)

        if difference <= 0:
            return max_health
        # todo change (60) by variable that consist time for which will regen one life
        return max_health - int(difference / 60)

    @staticmethod
    def health_to_time(current_health: int, max_health: int) -> int:
        now = time.time()

        missing_health = max_health - current_health

        # todo change (60) by variable that consist time for which will regen one life
        seconds_to_regen = now + (missing_health * 60)

        return int(seconds_to_regen)


hero_system = HeroSystem()
