from clan_event.lifeform_types.enemy_type import Enemy
from discord import Embed, Colour

from clan_event.lifeform_types.hero_type import Hero


class HeroInventoryView(object):
    def __init__(self, hero: Hero):
        self._embed = Embed(title=f'{hero.name} inventory: ', color=Colour(0x292b2f))
        for item in hero.inventory.items:
            self._embed.add_field(name=item.name, value=item.type)

        # for item in hero.inventory.equipped.slots.values():
        #     self._embed.add_field(name=item.name, value=item.type)

    @property
    def embed(self):
        return self._embed

