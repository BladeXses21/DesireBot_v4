from clan_event.lifeform_types.enemy_type import Enemy
from discord import Embed, Colour


class BossView(object):
    def __init__(self, enemy: Enemy):
        self._embed = Embed(title=f'Enemy {enemy.name}', color=Colour(0x292b2f))
        self._embed.add_field(name='attack_dmg', value=enemy.attack_dmg)
        self._embed.add_field(name='health', value=enemy.max_health)
        self._embed.set_thumbnail(url=enemy.image)

    @property
    def embed(self):
        return self._embed
