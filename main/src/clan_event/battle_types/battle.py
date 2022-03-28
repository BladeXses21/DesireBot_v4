from pydantic import BaseModel
from typing import List

from clan_event.battle_types.battle_stats import BattleStat
from clan_event.lifeform_types.enemy_type import Enemy
from clan_event.lifeform_types.hero_type import Hero
from systems.boss_event_system.hero_system import hero_system


class Battle(BaseModel):
    enemy: Enemy
    stats: List[BattleStat] = []

    def fight_with(self, hero: Hero):
        if self.enemy.is_dead() or hero.is_dead():
            print("Enemy or hero is dead so fight cancelled")
            return False

        # deal dmg between boss and hero
        self.enemy.take_dmg(hero.get_dmg())
        hero.take_dmg(self.enemy.attack_dmg)

        if hero.current_health <= 0:
            hero.die()

        for battle_stat in self.stats:
            if battle_stat.hero_id == hero.id:
                battle_stat.record_dmg(hero.get_dmg())
                return True

        self.stats.append(BattleStat(hero_id=hero.id, dmg_dealt=hero.get_dmg()))
        return True

    def is_over(self):
        return self.enemy.is_dead()

    def drop_items(self):
        if self.enemy.inventory.items.__len__() <= 0:
            print(f"Nothing to drop from boss {self.enemy.name}")
            return

        for stat in self.stats:
            hero = hero_system.get_hero_by_id(stat.hero_id)
            hero.inventory.add_item(self.enemy.inventory.random_item())
            hero_system.modify_inventory(hero)

    def get_hero_dealt_dmg(self, user_id: int):
        for battle_stat in self.stats:
            if battle_stat.hero_id == user_id:
                return battle_stat.dmg_dealt
        return 0
