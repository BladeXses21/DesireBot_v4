from discord import User

from config import NEW_HERO_START_ATTACK, NEW_HERO_START_HEALTH
from clan_event.life_forms.hero_type import Hero
from systems.database_system import DatabaseSystem


class HeroSystem(DatabaseSystem):

    def create_new_hero(self, user: User):
        self.event_hero_collection.insert_one({
            'hero_id': user.id,
            'name': user.name,
            'health': NEW_HERO_START_HEALTH,
            'attack_dmg': NEW_HERO_START_ATTACK,
        })
        return True

    def get_hero_by_id(self, user_id: int):
        hero_data = self.event_hero_collection.find_one({'hero_id': user_id}, {})
        return Hero(hero_data['hero_id'], hero_data['name'], hero_data['health'], hero_data['attack_dmg'])

    def change_health(self, hero: Hero):
        self.event_hero_collection.update_one({'hero_id': hero.hero_id}, {"$set": {'health': hero.health}})
        return True


hero_system = HeroSystem()
