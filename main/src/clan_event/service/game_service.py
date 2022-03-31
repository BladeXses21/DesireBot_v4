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
        fight_view = view_builder.fight_view()
        if ctx is None:
            ctx = await self.client.get_application_context(interaction)

        battle = battle_system.get_current_battle()

        if battle.is_over():
            view_builder.button_attack.disabled = True

        async def attack_callback(interact: Interaction):
            if battle.is_over():
                view_builder.button_attack.disabled = True
            await self.attack_enemy(interact, ctx)

        async def profile_callback(interact: Interaction):
            await self.profile(interact, ctx)

        view_builder.button_attack.callback = attack_callback
        view_builder.button_profile.callback = profile_callback

        if interaction.message is None:
            await interaction.response.send_message(embed=BattleEmbed(battle, interaction.user).embed,
                                                    view=fight_view)
        else:
            await interaction.response.edit_message(embed=BattleEmbed(battle, interaction.user).embed,
                                                    view=fight_view)

    async def profile(self, interaction: Interaction, ctx: ApplicationContext = None):
        profile_view = view_builder.profile_view()

        if ctx is None:
            ctx = await self.client.get_application_context(interaction)

        hero = hero_system.get_hero_by_user(ctx.user)

        async def inventory_callback(interact: Interaction):
            await self.inventory(interact, ctx)  # inventory command update view by yourself

        async def back_callback(interact: Interaction):
            await self.boss(interact, ctx)

        view_builder.button_back.callback = back_callback
        view_builder.button_inventory.callback = inventory_callback

        if interaction.message is None:
            await interaction.response.send_message(embed=HeroStatsEmbed(hero).embed, view=profile_view)
        else:
            await interaction.response.edit_message(embed=HeroStatsEmbed(hero).embed, view=profile_view)

    async def inventory(self, interaction: Interaction, ctx: ApplicationContext = None):
        inventory_view = view_builder.inventory_view()
        if ctx is None:
            ctx = await self.client.get_application_context(interaction)

        hero = hero_system.get_hero_by_user(ctx.user)

        async def back_callback(interact: Interaction):
            await self.profile(interact, ctx)

        async def up_callback(interact: Interaction):
            await self.inventory(interact, ctx)

        async def down_callback(interact: Interaction):
            await self.inventory(interact, ctx)

        async def equip_callback(interact: Interaction):
            await self.equip(interact, ctx, 1)

        view_builder.button_back.callback = back_callback
        view_builder.up_inventory_btn.callback = up_callback
        view_builder.down_inventory_btn.callback = down_callback
        view_builder.equip_btn.callback = equip_callback

        # todo change 1 on real id of selected item
        if interaction.message is None:
            await interaction.response.send_message(embed=HeroInventoryEmbed(hero, 1).embed, view=inventory_view)
        else:
            await interaction.response.edit_message(embed=HeroInventoryEmbed(hero, 1).embed, view=inventory_view)

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
            await interaction.response.send_message(embed=BattleEmbed(battle, interaction.user).embed)
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
            await interaction.response.send_message(embed=HeroInventoryEmbed(hero, index).embed)
        else:
            await interaction.response.edit_message(embed=HeroInventoryEmbed(hero, index).embed)

