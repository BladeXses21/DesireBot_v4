from discord import Embed, Colour

from game_event.model.lifeform_types.enemy_type import Enemy
from game_event.model.lifeform_types.hero_type import Hero


class BossesEmbed(object):
    def __init__(self, bosses: list[Enemy], selected: int):
        self.cursor = '<:arrow:959084748796465222>'
        self._embed = Embed(title=f'Game bosses: ', color=Colour(0xe42626))

        bosses_string = f""
        i = 1
        for boss in bosses:
            if i == selected:
                bosses_string = f'{bosses_string}\n{self.cursor} {i}.  {boss}'
            else:
                bosses_string = f"{bosses_string}\n{i}.  {boss}"
            i = i + 1
        self._embed.description = f"{bosses_string}"

    @property
    def embed(self):
        return self._embed
