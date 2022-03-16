from clan_event.lifeform_types.enemy_type import Enemy
from discord import Embed, Colour

from clan_event.lifeform_types.hero_type import Hero


class HeroStatsView(object):
    def __init__(self, hero: Hero):
        self._embed = Embed(title=f'{hero.name} stats: ', color=Colour(0x292b2f))
        self._embed.add_field(name='Health', value=hero.current_health)
        self._embed.add_field(name='Weapon Power', value=hero.attack_dmg)

    @property
    def embed(self):
        return self._embed
