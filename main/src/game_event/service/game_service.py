from discord import ApplicationContext, Interaction
from discord.ui import View

from embeds.boss_event.battle_embed import BattleEmbed
from embeds.boss_event.hero_embed import HeroStatsEmbed
from embeds.boss_event.hit_embed import HitEmbed
from embeds.boss_event.inventory_embed import HeroInventoryEmbed
from embeds.def_embed import DefaultEmbed
from embeds.view.view_builder import view_builder
from systems.boss_event_system.battle_system import battle_system
from systems.boss_event_system.hero_system import hero_system


class GameService:
    def __init__(self, client):
        self.client = client

    async def boss(self, interaction: Interaction, ctx: ApplicationContext = None):
        if ctx is None:
            ctx = await self.client.get_application_context(interaction)

        battle = battle_system.get_current_battle()

        view_builder.button_attack.disabled = battle.is_over()

        async def attack_callback(interact: Interaction):
            view_builder.button_attack.disabled = battle.is_over()
            await self.attack_enemy(interact, ctx)

        async def profile_callback(interact: Interaction):
            await self.profile(interact, ctx)

        fight_view = view_builder.fight(attack_callback, profile_callback)

        if interaction.message is None:
            await interaction.response.send_message(embed=BattleEmbed(battle, interaction.user).embed,
                                                    view=fight_view, ephemeral=True)
        else:
            await interaction.response.edit_message(embed=BattleEmbed(battle, interaction.user).embed,
                                                    view=fight_view)

    async def profile(self, interaction: Interaction, ctx: ApplicationContext = None):
        if ctx is None:
            ctx = await self.client.get_application_context(interaction)

        hero = hero_system.get_hero_by_user(ctx.user)

        async def inventory_callback(interact: Interaction):
            await self.inventory(interact, ctx)  # inventory command update view by yourself

        async def back_callback(interact: Interaction):
            await self.boss(interact, ctx)

        profile_view = view_builder.profile(back_callback, inventory_callback)

        if interaction.message is None:
            await interaction.response.send_message(embed=HeroStatsEmbed(hero).embed, view=profile_view, ephemeral=True)
        else:
            await interaction.response.edit_message(embed=HeroStatsEmbed(hero).embed, view=profile_view)

    async def inventory(self, interaction: Interaction, ctx: ApplicationContext = None, index: int = 1):
        if ctx is None:
            ctx = await self.client.get_application_context(interaction)

        hero = hero_system.get_hero_by_user(ctx.user)
        inventory = hero.inventory

        index = len(inventory.items) if index < 1 else 1 if index > len(inventory.items) else index

        async def back_callback(interact: Interaction):
            await self.profile(interact, ctx)

        async def up_callback(interact: Interaction):
            await self.inventory(interact, ctx, index - 1)

        async def down_callback(interact: Interaction):
            await self.inventory(interact, ctx, index + 1)

        async def equip_callback(interact: Interaction):
            await self.equip(interact, ctx, index)

        inventory_view = view_builder.inventory(back_callback, up_callback, down_callback, equip_callback)

        # todo change 1 on real id of selected item
        if interaction.message is None:
            await interaction.response.send_message(embed=HeroInventoryEmbed(hero, index).embed,
                                                    view=inventory_view, ephemeral=True)
        else:
            await interaction.response.edit_message(embed=HeroInventoryEmbed(hero, index).embed,
                                                    view=inventory_view)

    async def attack_enemy(self, interaction: Interaction, ctx: ApplicationContext = None):
        if ctx is None:
            ctx = await self.client.get_application_context(interaction)

        hero = hero_system.get_hero_by_user(ctx.user)
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

        await interaction.channel.send(embed=HitEmbed(hero).embed, delete_after=4)

        if interaction.message is None:
            await interaction.response.send_message(embed=BattleEmbed(battle, interaction.user).embed, ephemeral=True)
        else:
            await interaction.response.edit_message(embed=BattleEmbed(battle, interaction.user).embed)

    async def equip(self, interaction: Interaction, ctx: ApplicationContext = None, index: int = 1):
        if ctx is None:
            ctx = await self.client.get_application_context(interaction)

        hero = hero_system.get_hero_by_user(ctx.user)
        item_by_index = hero.inventory.item_by_index(index)

        if item_by_index is not None:
            hero.inventory.equip(item_by_index)
            hero_system.modify_inventory(hero)

        if interaction.message is None:
            await interaction.response.send_message(embed=HeroInventoryEmbed(hero, index).embed, ephemeral=True)
        else:
            await interaction.response.edit_message(embed=HeroInventoryEmbed(hero, index).embed)
