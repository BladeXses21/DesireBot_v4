import time
from datetime import datetime

from discord import User

from clan_event.inventory_types.hero_inventory import HeroInventory
from clan_event.inventory_types.inventory_type import Inventory
from config import NEW_HERO_START_ATTACK, NEW_HERO_START_HEALTH, NEW_HERO_START_INVENTORY
from clan_event.lifeform_types.hero_type import Hero
from systems.database_system import DatabaseSystem


class HeroSystem(DatabaseSystem):

    def create_new_hero(self, user: User):
        self.event_hero_collection.insert_one({
            'hero_id': user.id,
            'name': user.name,
            'regen_time': time.time(),
            'max_health': NEW_HERO_START_HEALTH,
            'attack_dmg': NEW_HERO_START_ATTACK,
            'inventory': NEW_HERO_START_INVENTORY.__dict__
            # 'inventory': {
            #     'equipped': NEW_HERO_START_INVENTORY.equipped.slots,
            #     'items': NEW_HERO_START_INVENTORY.items,
            #     'size': NEW_HERO_START_INVENTORY.max_size
            # },
        })
        return True

    def get_hero_by_user(self, user: User):
        hero_data = self.event_hero_collection.find_one({'hero_id': user.id}, {})

        # if user exist return him
        if hero_data is not None:
            return Hero(hero_data['hero_id'], hero_data['name'],
                        self.time_to_health(hero_data['regen_time'], hero_data['max_health']),
                        hero_data['max_health'], hero_data['attack_dmg'], hero_data['inventory'])

        hero_system.create_new_hero(user)
        hero_data = self.event_hero_collection.find_one({'hero_id': user.id}, {})
        return Hero(hero_data['hero_id'], hero_data['name'],
                    self.time_to_health(hero_data['regen_time'], hero_data['max_health']),
                    hero_data['max_health'], hero_data['attack_dmg'], hero_data['inventory'])

    def change_health(self, hero: Hero):
        self.event_hero_collection.update_one({'hero_id': hero.hero_id},
                                              {"$set": {'regen_time': self.health_to_time(hero.current_health
                                                                                          , hero.max_health)
                                                        }})
        return True

    def change_inventory(self, hero: Hero):
        self.event_hero_collection.update_one({'hero_id': hero.hero_id},
                                              {"$set": {'inventory': hero.inventory}})
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
