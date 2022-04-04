from discord import Embed, Colour

from embeds.boss_event.battle_embed import BattleEmbed
from game_event.model.battle_types.battle import Battle
from game_event.model.lifeform_types.hero_type import Hero


class HitEmbed(BattleEmbed):
    def __init__(self, battle: Battle, hero: Hero):
        super().__init__(battle, hero.id)
        self.color = Colour(0x292b2f)
        self.set_image(
            url="https://cdn.discordapp.com/attachments/952010583388074044/960474136071798814/ezgif.com-gif-maker_1.gif")
