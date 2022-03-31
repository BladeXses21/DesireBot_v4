import discord
from discord.ui import View, Button


class ViewBuilder:
    def __init__(self):
        self.button_attack = Button(style=discord.ButtonStyle.green, label='Attack', emoji="🗡")
        self.button_profile = Button(style=discord.ButtonStyle.blurple, label='Profile', emoji="🗡")

        self.button_inventory = Button(style=discord.ButtonStyle.secondary, label='Inventory', emoji='🧳')
        self.button_stats = Button(style=discord.ButtonStyle.secondary, label='Stats', emoji='💎')
        self.button_back = Button(style=discord.ButtonStyle.red, label='Back', emoji='ℹ')

        self.up_inventory_btn = Button(style=discord.ButtonStyle.secondary, label=':arrow_up:', emoji='⬆')
        self.down_inventory_btn = Button(style=discord.ButtonStyle.secondary, label=':arrow_down:', emoji='⬇')
        self.equip_btn = Button(style=discord.ButtonStyle.green, label='Equip')

    def fight_view(self) -> View:
        fight_view = View()
        fight_view.add_item(self.button_attack)
        fight_view.add_item(self.button_profile)
        return fight_view

    def profile_view(self) -> View:
        profile_view = View()
        profile_view.add_item(self.button_back)
        profile_view.add_item(self.button_inventory)
        return profile_view

    def inventory_view(self) -> View:
        inventory_view = View()
        inventory_view.add_item(self.button_back)
        inventory_view.add_item(self.up_inventory_btn)
        inventory_view.add_item(self.down_inventory_btn)
        inventory_view.add_item(self.equip_btn)
        return inventory_view


view_builder = ViewBuilder()
