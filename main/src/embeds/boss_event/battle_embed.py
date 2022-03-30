from math import ceil

from clan_event.battle_types.battle import Battle
from discord import Embed, Colour, User

from clan_event.heart_bar.boss_heath_bar import BossHealthBarCreator
from systems.boss_event_system.hero_system import hero_system


class BattleView(object):
    def __init__(self, battle: Battle, user: User):
        self._embed = Embed(title='Кланова гра', color=Colour(0x9006d0))
        enemy = battle.enemy

        pool_length = 13
        red_pool = ceil(enemy.current_health / (enemy.max_health / pool_length))
        health_bar = BossHealthBarCreator(red_pool, pool_length)

        self._embed.description = f"**{enemy.name}**\n\n" \
                                  f"{enemy.current_health}/{enemy.max_health}\n" \
                                  f"{health_bar.__str__()}\n\n" \
                                  f"**Ти наніс -**  {battle.get_hero_dealt_dmg(user.id)} ⚔\n"

        self._embed.add_field(name='Top 3', value='heroes', inline=True)

        sorted_stats = sorted(battle.stats, key=lambda x: x.dmg_dealt, reverse=True)
        for i in range(0, -3):
            if i > 3:
                break
            hero_stat = sorted_stats.pop()

            if hero_stat is not None:
                self._embed.add_field(name=f'{hero_system.name_by_id(hero_stat.hero_id)}',
                                      value=f'{hero_stat.dmg_dealt} ⚔', inline=True)

        if battle.enemy.is_dead():
            self._embed.set_image(
                url="https://cdn.discordapp.com/attachments/866061390313029666/958691305427451966/death-killing.gif")
            return

        self._embed.set_image(url=enemy.image)

    @property
    def embed(self):
        return self._embed
