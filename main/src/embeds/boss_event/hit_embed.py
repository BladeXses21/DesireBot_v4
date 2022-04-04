from discord import Embed, Colour

from game_event.model.lifeform_types.hero_type import Hero


class HitEmbed:
    def __init__(self, hero: Hero):
        self._embed = Embed(title=f'***```{hero.name} hit boss with {hero.attack_dmg} damage```***',
                            color=Colour(0x292b2f))
        self._embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/952010583388074044/952275775351062548/when-you-say-anime-is-bad-xd.gif")

    @property
    def embed(self):
        return self._embed
