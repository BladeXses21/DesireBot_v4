from math import ceil

from discord import Embed, Colour

from game_event.model.battle_types.battle import Battle

from game_event.model.heart_bar.boss_heath_bar import BossHealthBarCreator
from game_event.model.lifeform_types.hero_type import Hero
from systems.boss_event_system.hero_system import hero_system


class BattleEmbed(Embed):
    def __init__(self, battle: Battle, hero_id: int):
        super().__init__(title='Кланова гра', color=Colour(0x9006d0))
        pool_length = 13
        enemy = battle.enemy

        red_pool = ceil(enemy.current_health / (enemy.max_health / pool_length))
        health_bar = BossHealthBarCreator(red_pool, pool_length)

        self.description = f"**{enemy.name}**\n\n" \
                           f"{enemy.current_health}/{enemy.max_health}\n" \
                           f"{health_bar}\n\n" \
                           f"**Ти наніс -**  {battle.get_hero_dealt_dmg(hero_id)} ⚔\n"

        self.add_field(name='Top 3', value='heroes', inline=True)

        sorted_stats = sorted(battle.stats, key=lambda x: x.dmg_dealt, reverse=True)
        for i in range(0, -3):
            if i > 3:
                break
            hero_stat = sorted_stats.pop()

            if hero_stat is not None:
                self.add_field(name=f'{hero_system.name_by_id(hero_stat.hero_id)}',
                               value=f'{hero_stat.dmg_dealt} ⚔', inline=True)

        if enemy.is_dead():
            self.set_image(
                url="https://cdn.discordapp.com/attachments/866061390313029666/958691305427451966/death-killing.gif")
            return

        self.set_image(url=enemy.image)
