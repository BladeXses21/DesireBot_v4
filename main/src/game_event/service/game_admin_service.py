from discord import Interaction, ApplicationContext

from embeds.boss_event.boss_drop_embed import BossDropEmbed
from embeds.boss_event.boss_embed import BossEmbed
from embeds.boss_event.bosses_embed import BossesEmbed
from embeds.boss_event.game_items_embed import GameItemsEmbed
from embeds.def_embed import DefaultEmbed
from embeds.view.add_items import AddItemsView
from embeds.view.admin_menu import AdminMenuView
from embeds.view.boss import BossView
from embeds.view.bosses import BossesView
from game_event.model.lifeform_types.enemy_type import Enemy
from systems.boss_event_system.boss_system import boss_system
from systems.boss_event_system.items_system import items_system


class GameAdminService:
    def __init__(self, client):
        self.client = client

    async def admin_menu(self, interaction: Interaction):
        async def enemies_callback(interact: Interaction):
            await self.game_enemies(interact)

        async def items_callback(interact: Interaction):
            await self.game_enemies(interact)

        async def heroes_callback(interact: Interaction):
            await self.game_enemies(interact)

        bosses_view = AdminMenuView(enemies_callback, items_callback, heroes_callback)

        if interaction.message is None:
            await interaction.response.send_message(embed=None, view=bosses_view, ephemeral=True)
        else:
            await interaction.response.edit_message(embed=None, view=bosses_view)

        # todo admin menu

    async def game_enemies(self, interaction: Interaction, index: int = 1):
        bosses = boss_system.all_bosses()
        index = len(bosses) if index < 1 else 1 if index > len(bosses) else index

        # todo create admin menu
        async def back_callback(interact: Interaction):
            await self.admin_menu(interact)

        async def up_callback(interact: Interaction):
            await self.game_enemies(interact, index - 1)

        async def down_callback(interact: Interaction):
            await self.game_enemies(interact, index + 1)

        async def choose_callback(interact: Interaction):
            if len(bosses) <= 0:
                return
            boss_name = bosses.__getitem__(index - 1).name
            await self.enemy(interact, boss_name)

        bosses_view = BossesView(back_callback, up_callback, down_callback, choose_callback)

        if interaction.message is None:
            await interaction.response.send_message(embed=BossesEmbed(bosses, index).embed,
                                                    view=bosses_view,
                                                    ephemeral=True)
        else:
            await interaction.response.edit_message(embed=BossesEmbed(bosses, index).embed,
                                                    view=bosses_view)

    async def enemy(self, interaction: Interaction, enemy_name: str):
        boss = boss_system.get_by_name(enemy_name)
        if boss is None:
            return

        async def back_callback(interact: Interaction):
            await self.game_enemies(interact)

        async def add_items_callback(interact: Interaction):
            print('trying to add items to boss')
            await self.boss_add_items(interact, enemy_name)

        async def delete_callback(interact: Interaction):
            await self.delete_boss(interact, enemy_name)

        boss_view = BossView(back_callback, add_items_callback, delete_callback)

        if interaction.message is None:
            await interaction.response.send_message(embed=BossEmbed(boss).embed, view=boss_view, ephemeral=True)
        else:
            await interaction.response.edit_message(embed=BossEmbed(boss).embed, view=boss_view)

    async def delete_boss(self, interaction: Interaction, enemy_name: str):
        boss_system.remove_by_name(enemy_name)
        await self.game_enemies(interaction)

    async def boss_add_items(self, interaction: Interaction, enemy_name: str, index: int = 1):
        items = items_system.all_items()
        if items is None:
            return
        index = len(items) if index < 1 else 1 if index > len(items) else index

        async def back_enemies_callback(interact: Interaction):
            await self.game_enemies(interact)

        async def back_callback(interact: Interaction):
            await self.enemy(interact, enemy_name)

        async def up_callback(interact: Interaction):
            await self.boss_add_items(interact, enemy_name, index - 1)

        async def down_callback(interact: Interaction):
            await self.boss_add_items(interact, enemy_name, index + 1)

        async def add_callback(interact: Interaction):
            item_name = items.__getitem__(index - 1).name
            await self.add_drop(interact, enemy_name, item_name)

        if enemy_name is None:
            items_view = AddItemsView(back_enemies_callback, up_callback, down_callback, add_callback, add_callback)
        else:
            items_view = AddItemsView(back_callback, up_callback, down_callback, add_callback, add_callback)

        if interaction.message is None:
            await interaction.response.send_message(embed=GameItemsEmbed(items, index).embed, view=items_view,
                                                    ephemeral=True)
        else:
            await interaction.response.edit_message(embed=GameItemsEmbed(items, index).embed, view=items_view)

    async def add_drop(self, interaction: Interaction, boss_name: str, item_name: str):
        boss = boss_system.get_by_name(boss_name)
        inventory = boss.inventory
        item = items_system.find_by_name(item_name)
        if item is None:
            await interaction.response.send_message(embed=DefaultEmbed("```Item doesnt exist```"))
            return
        inventory.add_item(item)

        boss_system.modify_inventory(boss)
        await self.enemy(interaction, boss_name)
