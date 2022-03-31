import discord
from discord import Option, Interaction, Bot, Embed, ApplicationContext
from discord.commands import slash_command

from clan_event.service.game_service import GameService
from embeds.boss_event.battle_embed import BattleEmbed
from embeds.boss_event.inventory_embed import HeroInventoryEmbed
from embeds.def_embed import DefaultEmbed
from config import ClANS_GUILD_ID, PREFIX
from cogs.base import BaseCog
from embeds.boss_event.hit_embed import HitEmbed
from embeds.view.view_builder import ViewBuilder, view_builder
from systems.boss_event_system.battle_system import battle_system
from systems.boss_event_system.hero_system import hero_system


class BossGamePlayer(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.game_service = GameService(bot)
        print("Cog 'boss-game player commands' connected!")

    @slash_command(name='boss', description='Start Boss Embed', guild_ids=[ClANS_GUILD_ID])
    async def boss(self, interaction: Interaction):
        await self.game_service.boss(interaction)

    @slash_command(name='attack_enemy', description='Attack enemy', guild_ids=[ClANS_GUILD_ID])
    async def attack_enemy(self, interaction: Interaction):
        await self.game_service.attack_enemy(interaction)

    @slash_command(name='profile', description='Show user stats in boss event', guild_ids=[ClANS_GUILD_ID])
    async def profile(self, interaction: Interaction):
        await self.game_service.profile(interaction)

    @slash_command(name='inventory', description='Show your inventory', guild_ids=[ClANS_GUILD_ID])
    async def inventory(self, interaction: Interaction):
        await self.game_service.inventory(interaction)

    @slash_command(name='equip_item', description='equip item from your inventory', guild_ids=[ClANS_GUILD_ID])
    async def equip_item(self, interaction: Interaction, item_index: int):
        await self.game_service.equip(interaction=interaction, index=item_index)

    @slash_command(name='remove_item', description='remove item from your inventory', guild_ids=[ClANS_GUILD_ID])
    async def remove_item(self, interaction: Interaction, item_index: int):
        hero = hero_system.get_hero_by_user(interaction.user)
        inventory = hero.inventory
        inventory.remove_item(item_index)

        hero_system.modify_inventory(hero)
        await interaction.response.send_message(embed=HeroInventoryEmbed(hero).embed)


def setup(bot: Bot):
    bot.add_cog(BossGamePlayer(bot))
