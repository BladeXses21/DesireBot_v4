from pydantic import BaseModel
from typing import List

from game_event.model.battle_types.dmg_record import DmgRecord
from game_event.model.lifeform_types.enemy_type import Enemy
from game_event.model.lifeform_types.hero_type import Hero
from systems.boss_event_system.hero_system import hero_system


class Battle(BaseModel):
    enemy: Enemy
    stats: List[DmgRecord] = []

    def fight_with(self, hero: Hero):
        if self.enemy.is_dead() or hero.is_dead():
            print("Enemy or hero is dead so fight cancelled")
            return False

        # deal dmg between boss and hero
        self.enemy.take_dmg(hero.get_dmg())
        hero.take_dmg(self.enemy.attack_dmg)

        self.record_dealt_dmg(hero.id, hero.get_dmg())

        if self.enemy.is_dead():
            self.drop_items()
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

    def record_dealt_dmg(self, hero_id: int, dmg: int):
        dmg_record = None
        for record in self.stats:
            if record.hero_id == hero_id:
                dmg_record = record

        if dmg_record is not None:
            dmg_record.record_dmg(dmg)
        else:
            self.stats.append(DmgRecord(hero_id=hero_id, dmg_dealt=dmg))

    def get_hero_dealt_dmg(self, user_id: int):
        for battle_stat in self.stats:
            if battle_stat.hero_id == user_id:
                return battle_stat.dmg_dealt
        return 0
