from pydantic import BaseModel
from typing import List

from clan_event.battle_types.battle_stats import BattleStat
from clan_event.lifeform_types.enemy_type import Enemy
from clan_event.lifeform_types.hero_type import Hero


class Battle(BaseModel):
    enemy: Enemy
    stats: List[BattleStat] = []

    def fight_with(self, hero: Hero):
        # deal dmg between boss and hero
        dmg = hero.attack_dmg
        self.enemy.take_dmg(dmg)
        hero.take_dmg(self.enemy.attack_dmg)

        for battle_stat in self.stats:
            if battle_stat.hero_id == hero.get_id():
                battle_stat.dmg_dealt = battle_stat.dmg_dealt + dmg
                return

        self.stats.append(BattleStat(hero_id=hero.get_id(), dmg_dealt=dmg))

    def get_hero_dealt_dmg(self, user_id: int):
        for battle_stat in self.stats:
            if battle_stat.hero_id == user_id:
                return battle_stat.dmg_dealt
        return 0