import time
from math import ceil

from discord import Embed, Colour

from game_event.model.lifeform_types.hero_type import Hero
from game_event.model.heart_bar.health_bar import HealthBarCreator


class HeroStatsEmbed(object):
    def __init__(self, hero: Hero):
        self._embed = Embed(title=f'{hero.name} stats: ', color=Colour(0x292b2f))

        hearts_length = 15
        red_pool = ceil(hero.current_health / (hero.max_health / hearts_length))
        health_pool = HealthBarCreator(red_pool, hearts_length)

        self._embed.add_field(name=f"{hero.current_health}/{hero.max_health}\n", value=f'{health_pool.__str__()}')
        self._embed.add_field(name='Weapon Power', value=hero.attack_dmg, inline=False)
        if hero.is_dead():
            self._embed.set_thumbnail(url= 'https://cdn.discordapp.com/attachments/952010583388074044/960522617855549491/unknown.png')
            self._embed.add_field(name='Resurrection after',
                                  value=f"{int((hero.respawn_time - time.time()) / 3600)} hours", inline=False)

    @property
    def embed(self):
        return self._embed
