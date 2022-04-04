from game_event.model.lifeform_types.enemy_type import Enemy
from discord import Embed, Colour


class BossEmbed(object):
    def __init__(self, enemy: Enemy):
        self._embed = Embed(title=f'Enemy {enemy.name}', color=Colour(0x292b2f))
        self._embed.add_field(name='attack_dmg', value=enemy.attack_dmg)
        self._embed.add_field(name='health', value= f"{enemy.current_health}/{enemy.max_health}")

        inventory = enemy.inventory

        items_string = ''
        i = 1
        for item in inventory.items:
            items_string = f"{items_string}\n{i}. {item}"
            i += 1
        self._embed.description = f"{items_string}"

        self._embed.set_thumbnail(url=enemy.image)

    @property
    def embed(self):
        return self._embed
