import discord
from discord import Option, Interaction, Bot, Embed
from discord.commands import slash_command
from discord.ui import Button, View
from discord.ext import commands
from embeds.boss_event.battle_embed import BattleView
from embeds.boss_event.boss_drop_embed import BossDropView
from embeds.boss_event.heal_embed import HealView
from embeds.boss_event.inventory_embed import HeroInventoryView
from embeds.def_embed import DefaultEmbed
from clan_event.inventory_types.item_type import EnumItemTypes, Item
from config import ClANS_GUILD_ID, PREFIX
from embeds.boss_event.boss_embed import BossView
from cogs.base import BaseCog
from embeds.boss_event.hero_embed import HeroStatsView
from embeds.boss_event.hit_embed import HitView
from systems.boss_event_system.battle_system import battle_system
from systems.boss_event_system.hero_system import hero_system


class BossGamePlayer(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        print("Cog 'boss-game player commands' connected!")

    @slash_command(name='boss', description='Start Boss Embed', guild_ids=[ClANS_GUILD_ID])
    async def boss(self, interaction: Interaction):
        button_attack = Button(style=discord.ButtonStyle.green, label='Attack', emoji="🗡")
        button_inventory = Button(style=discord.ButtonStyle.secondary, label='Inventory', emoji='🧳')
        button_stats = Button(style=discord.ButtonStyle.red, label='Stats', emoji='💎')
        button_boss = Button(style=discord.ButtonStyle.blurple, label='Boss Info', emoji='ℹ')

        # fight_view = View(*[button_attack, button_inventory, button_stats])
        fight_view = View()
        other_view = View()

        fight_view.add_item(button_attack)
        fight_view.add_item(button_inventory)
        fight_view.add_item(button_stats)

        other_view.add_item(button_boss)
        other_view.add_item(button_inventory)
        other_view.add_item(button_stats)

        battle = battle_system.get_current_battle()

        if battle.is_over():
            button_attack.disabled = True

        async def attack_callback(interact: Interaction):
            ctx = await self.client.get_application_context(interact)
            if battle.is_over():
                button_attack.disabled = True
            await interact.message.edit(view=fight_view)
            await self.attack_enemy(ctx=ctx, interaction=interact)

        async def stats_callback(interact: Interaction):
            ctx = await self.client.get_application_context(interact)
            await interact.message.edit(view=other_view)
            await self.my_stats(ctx=ctx, interaction=interact)

        async def inventory_callback(interact: Interaction):
            ctx = await self.client.get_application_context(interact)
            await interact.message.edit(view=other_view)
            await self.inventory(ctx=ctx, interaction=interact)

        async def boss_info_callback(interact: Interaction):
            await interact.response.edit_message(
                embed=BattleView(battle_system.get_current_battle(), interaction.user).embed, view=fight_view)

        button_attack.callback = attack_callback
        button_stats.callback = stats_callback
        button_inventory.callback = inventory_callback
        button_boss.callback = boss_info_callback

        await interaction.response.send_message(embed=BattleView(battle, interaction.user).embed,
                                                view=fight_view)

    @slash_command(name='attack_enemy', description='Attack enemy', guild_ids=[ClANS_GUILD_ID])
    async def attack_enemy(self, interaction: Interaction):
        hero = hero_system.get_hero_by_user(interaction.user)
        if hero.is_dead():
            # todo create better embed for displaying dead hero
            await interaction.response.send_message(embed=DefaultEmbed(f'***```You cant attack being dead !!!```***'),
                                                    delete_after=3,
                                                    ephemeral=True)
            return

        battle = battle_system.get_current_battle()

        if not battle.fight_with(hero):
            await interaction.response.send_message(embed=DefaultEmbed(description="***```Boss already dead```***"),
                                                    ephemeral=True)
            return

        battle_system.update_current_battle(battle)
        hero_system.health_change(hero)

        await interaction.channel.send(embed=HitView(hero).embed, delete_after=4)

        if interaction.message.components is not None:
            await interaction.response.edit_message(embed=BattleView(battle, interaction.user).embed)
        else:
            await interaction.response.send_message(embed=BattleView(battle, interaction.user).embed, ephemeral=True)

    @slash_command(name='stats', description='Show user stats in boss event', guild_ids=[ClANS_GUILD_ID])
    async def my_stats(self, interaction: discord.Interaction):
        hero = hero_system.get_hero_by_user(interaction.user)

        if interaction.message.components is not None:
            await interaction.response.edit_message(embed=HeroStatsView(hero).embed)
        else:
            await interaction.response.send_message(embed=HeroStatsView(hero).embed, ephemeral=True)

    @slash_command(name='inventory', description='Show your inventory', guild_ids=[ClANS_GUILD_ID])
    async def inventory(self, interaction: discord.Interaction):
        hero = hero_system.get_hero_by_user(interaction.user)
        if interaction.message.components is not None:
            await interaction.response.edit_message(embed=HeroInventoryView(hero).embed)
        else:
            await interaction.response.send_message(embed=HeroInventoryView(hero).embed, ephemeral=True)

    @slash_command(name='equip_item', description='equip item from your inventory', guild_ids=[ClANS_GUILD_ID])
    async def equip_item(self, interaction: discord.Interaction, item_index: int):
        hero = hero_system.get_hero_by_user(interaction.user)
        inventory = hero.inventory
        inventory.equip(inventory.item_by_index(item_index))

        hero_system.modify_inventory(hero)
        await interaction.response.send_message(embed=HeroInventoryView(hero).embed)

    @slash_command(name='remove_item', description='remove item from your inventory', guild_ids=[ClANS_GUILD_ID])
    async def remove_item(self, interaction: discord.Interaction, item_index: int):
        hero = hero_system.get_hero_by_user(interaction.user)
        inventory = hero.inventory
        inventory.remove_item(item_index)

        hero_system.modify_inventory(hero)
        await interaction.response.send_message(embed=HeroInventoryView(hero).embed)


def setup(bot: Bot):
    bot.add_cog(BossGamePlayer(bot))
