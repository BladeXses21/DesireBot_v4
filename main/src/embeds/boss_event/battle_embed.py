import cmath
from math import floor

from clan_event.battle_types.battle import Battle
from clan_event.lifeform_types.enemy_type import Enemy
from discord import Embed, Colour, User

from systems.boss_event_system.hero_system import hero_system


class BattleView(object):
    def __init__(self, battle: Battle, user: User):
        self._embed = Embed(title='Кланова гра', color=Colour(0x9006d0))
        enemy = battle.enemy
        number_of_hearts = floor(enemy.current_health / (enemy.max_health / 23))
        self._embed.description = f"**{enemy.name}**\n\n" \
                                  f"Здоров'я - {enemy.current_health}/{enemy.max_health}\n" \
                                  f"{'<:heart_purples:956343794595426304>' * number_of_hearts}\n\n" \
                                  f"**Ти наніс -**  {battle.get_hero_dealt_dmg(user.id)} ⚔\n"

        self._embed.add_field(name='Топ 3', value='героя', inline=True)

        sorted_stats = sorted(battle.stats, key=lambda x: x.dmg_dealt, reverse=True)
        for i in range(0, sorted_stats.__len__()):
            if i > 3:
                break
            hero_stat = sorted_stats.pop()

            if hero_stat is not None:
                self._embed.add_field(name=f'🥇 {hero_system.name_by_id(hero_stat.hero_id)}',
                                      value=f'{hero_stat.dmg_dealt} ⚔', inline=True)

        self._embed.set_image(url=enemy.image)

    @property
    def embed(self):
        return self._embed
