from clan_event.lifeform_types.enemy_type import Enemy
from discord import Embed, Colour

from clan_event.lifeform_types.hero_type import Hero


class HealView:
    def __init__(self, hero: Hero):
        self._embed = Embed(title=f'***```{hero.name} was healed to full. His now have {hero.current_health} life```***',
                            color=Colour(0x292b2f))
        self._embed.set_image(url="https://cdn.discordapp.com/attachments/866061390313029666/953745718248632340/ezgif.com-gif-maker.gif")

    @property
    def embed(self):
        return self._embed
