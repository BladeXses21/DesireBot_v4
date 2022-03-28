import discord
from discord import Option, Interaction, Bot
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
from systems.boss_event_system.boss_system import boss_system
from systems.boss_event_system.hero_system import hero_system
from systems.boss_event_system.items_system import items_system


async def default_respond(interaction):
    if not interaction.response.is_done():
        interaction.response.pong()


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

        view = discord.ui.View()

        view.add_item(button_stats)
        view.add_item(button_inventory)
        view.add_item(button_attack)

        async def attack_callback(interact: Interaction):
            ctx = await self.client.get_application_context(interact)
            await interact.message.edit(view=view)
            await self.attack_enemy(ctx=ctx, interaction=interact)

        async def stats_callback(interact: Interaction):
            ctx = await self.client.get_application_context(interact)
            view.remove_item(button_boss)
            view.remove_item(button_attack)
            view.add_item(button_boss)
            await interact.message.edit(view=view)
            await self.my_stats(ctx=ctx, interaction=interact)

        async def inventory_callback(interact: Interaction):
            ctx = await self.client.get_application_context(interact)
            view.remove_item(button_boss)
            view.remove_item(button_attack)
            view.add_item(button_boss)
            await interact.message.edit(view=view)
            await self.inventory(ctx=ctx, interaction=interact)

        async def boss_info_callback(interact: Interaction):
            view.remove_item(button_boss)
            view.add_item(button_attack)
            await interact.message.edit(view=view)
            await interact.response.edit_message(
                embed=BattleView(battle_system.get_current_battle(), interaction.user).embed)

        button_attack.callback = attack_callback
        button_stats.callback = stats_callback
        button_inventory.callback = inventory_callback
        button_boss.callback = boss_info_callback

        battle = battle_system.get_current_battle()

        await interaction.response.send_message(embed=BattleView(battle, interaction.user).embed,
                                                view=view)

    @slash_command(name='attack_enemy', description='Attack enemy', guild_ids=[ClANS_GUILD_ID])
    async def attack_enemy(self, interaction: Interaction):
        hero = hero_system.get_hero_by_user(interaction.user)
        if hero.is_dead():
            # todo create better embed for displaying dead hero
            await interaction.response.send_message(embed=DefaultEmbed(f'***```You cant attack being dead !!!```***'),
                                                    delete_after=3)
            return

        battle = battle_system.get_current_battle()

        if battle.is_over():
            boss = boss_system.get_random_boss()
            battle = battle_system.start_new_battle(boss)

            # todo embed for boss spawn
            await interaction.channel.send(
                embed=DefaultEmbed(f'***```Boss {boss.name} was born in hell to destroy the world!```***'))

        battle.fight_with(hero)

        battle_system.update_current_battle(battle)
        hero_system.health_change(hero)
        await interaction.channel.send(embed=HitView(hero).embed, delete_after=5)

        if battle.is_over():
            # todo embed for epic boss dead
            await interaction.channel.send(embed=DefaultEmbed(f'***Boss `{battle.enemy.name}` is dead!!!***'))
            return

        await interaction.response.edit_message(embed=BattleView(battle, interaction.user).embed)

        await default_respond(interaction)

    @slash_command(name='stats', description='Show user stats in boss event', guild_ids=[ClANS_GUILD_ID])
    async def my_stats(self, interaction: discord.Interaction):
        hero = hero_system.get_hero_by_user(interaction.user)
        await interaction.response.edit_message(embed=HeroStatsView(hero).embed)

    @slash_command(name='inventory', description='Show your inventory', guild_ids=[ClANS_GUILD_ID])
    async def inventory(self, interaction: discord.Interaction):
        hero = hero_system.get_hero_by_user(interaction.user)
        await interaction.response.edit_message(embed=HeroInventoryView(hero).embed)

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
