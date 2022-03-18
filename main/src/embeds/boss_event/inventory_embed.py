from clan_event.lifeform_types.enemy_type import Enemy
from discord import Embed, Colour

from clan_event.lifeform_types.hero_type import Hero


class HeroInventoryView(object):
    def __init__(self, hero: Hero):
        self._embed = Embed(title=f'{hero.name} inventory: ', color=Colour(0x292b2f))
        items_string = f"helmet : {hero.inventory.equipped.helmet}"
        items_string = f"{items_string}\ngloves : {hero.inventory.equipped.gloves}"
        items_string = f"{items_string}\nchest : {hero.inventory.equipped.chest}"
        items_string = f"{items_string}\npants : {hero.inventory.equipped.pants}"
        items_string = f"{items_string}\nboots : {hero.inventory.equipped.boots}\n"

        i = 1
        for item in hero.inventory.items:
            items_string = f"{items_string}\n{i}. {item.name}"
            i = i + 1
        self._embed.description = f"`{items_string}`"

    @property
    def embed(self):
        return self._embed
