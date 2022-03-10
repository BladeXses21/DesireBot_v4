from clan_event.boss_type import Enemy
from discord import Embed, Colour


class BossView(object):
    def __init__(self, enemy: Enemy):
        self._embed = Embed(title=f'Enemy {enemy.name}', color=Colour(0x292b2f))
        self._embed.add_field(name='atack_dmg', value=enemy.atack_dmg)
        self._embed.add_field(name='health', value=enemy.health)
        self._embed.set_thumbnail(url=enemy.image)

    @property
    def embed(self):
        return self._embed
