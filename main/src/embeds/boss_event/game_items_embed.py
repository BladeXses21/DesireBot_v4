from discord import Embed, Colour

from game_event.model.inventory_types.item_type import Item
from game_event.model.lifeform_types.hero_type import Hero


class GameItemsEmbed(object):
    def __init__(self, items: list[Item], selected: int):
        self.cursor = '<:arrow:959084748796465222>'
        self._embed = Embed(title=f'Items: ', color=Colour(0x292b2f))
        i = 1
        items_string = ''
        for item in items:
            if i == selected:
                items_string = f'{items_string}\n{self.cursor} {i}.  {item}'
            else:
                items_string = f"{items_string}\n{i}.  {item}"
            i = i + 1
        self._embed.description = f"{items_string}"

    @property
    def embed(self):
        return self._embed
