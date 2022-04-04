import discord
from discord.ui import View, Button


class ViewBuilder:
    def __init__(self):
        self.button_attack = Button(style=discord.ButtonStyle.green, label='Attack', emoji="🗡")
        self.button_profile = Button(style=discord.ButtonStyle.blurple, label='Profile', emoji="📖")

        self.button_inventory = Button(style=discord.ButtonStyle.secondary, label='Inventory', emoji='🧳')
        self.back_btn = Button(style=discord.ButtonStyle.secondary, label='', emoji='🔙')

        self.up_btn = Button(style=discord.ButtonStyle.secondary, label='', emoji='⬆')
        self.down_btn = Button(style=discord.ButtonStyle.secondary, label='', emoji='⬇')
        self.equip_btn = Button(style=discord.ButtonStyle.green, label='Equip')

        self.choose_btn = Button(style=discord.ButtonStyle.blurple, label='Choose')
        self.add_items_btn = Button(style=discord.ButtonStyle.secondary, label='Add items')
        self.delete_btn = Button(style=discord.ButtonStyle.red, label='Delete')

        self.detail = Button(style=discord.ButtonStyle.secondary, label='', emoji='ℹ')
        self.add_item_btn = Button(style=discord.ButtonStyle.blurple, label='', emoji='➕')

    def disable_fight(self):
        self.button_attack.disabled = True
        self.button_profile.disabled = True

    def enable_fight(self):
        self.button_attack.disabled = False
        self.button_profile.disabled = False

    def fight(self, attack_callback, profile_callback) -> View:
        fight_view = View(timeout=None)
        self.button_attack.callback = attack_callback
        self.button_profile.callback = profile_callback
        fight_view.add_item(self.button_attack)
        fight_view.add_item(self.button_profile)
        return fight_view

    def profile(self, back_callback, inventory_callback) -> View:
        profile_view = View(timeout=None)
        self.back_btn.callback = back_callback
        self.button_inventory.callback = inventory_callback
        profile_view.add_item(self.back_btn)
        profile_view.add_item(self.button_inventory)
        return profile_view

    def inventory(self, back_callback, up_callback, down_callback, equip_callback) -> View:
        inventory_view = View(timeout=None)
        self.back_btn.callback = back_callback
        self.up_btn.callback = up_callback
        self.down_btn.callback = down_callback
        self.equip_btn.callback = equip_callback
        inventory_view.add_item(self.back_btn)
        inventory_view.add_item(self.up_btn)
        inventory_view.add_item(self.down_btn)
        inventory_view.add_item(self.equip_btn)
        return inventory_view

    def bosses_view(self, back_callback, up_callback, down_callback, choose_callback) -> View:
        bosses_view = View(timeout=None)
        self.back_btn.callback = back_callback
        self.up_btn.callback = up_callback
        self.down_btn.callback = down_callback
        self.choose_btn.callback = choose_callback
        bosses_view.add_item(self.back_btn)
        bosses_view.add_item(self.up_btn)
        bosses_view.add_item(self.down_btn)
        bosses_view.add_item(self.choose_btn)
        return bosses_view

    def boss_view(self, back_callback, add_items_callback, delete_callback) -> View:
        bosses_view = View(timeout=None)
        self.back_btn.callback = back_callback
        self.add_items_btn.callback = add_items_callback
        self.delete_btn.callback = delete_callback
        bosses_view.add_item(self.back_btn)
        bosses_view.add_item(self.add_items_btn)
        bosses_view.add_item(self.delete_btn)
        return bosses_view

    def items_view(self, back_callback, detail_callback, delete_callback) -> View:
        items_view = View(timeout=None)
        self.back_btn.callback = back_callback
        self.detail.callback = detail_callback
        self.delete_btn.callback = delete_callback
        items_view.add_item(self.back_btn)
        items_view.add_item(self.detail)
        items_view.add_item(self.delete_btn)
        return items_view

    def boss_additems_view(self, back_callback, up_callback, down_callback, add_callback, detail_callback) -> View:
        bosses_view = View(timeout=None)
        self.back_btn.callback = back_callback
        self.up_btn.callback = up_callback
        self.down_btn.callback = down_callback
        self.add_item_btn.callback = add_callback
        self.detail.callback = detail_callback
        bosses_view.add_item(self.back_btn)
        bosses_view.add_item(self.up_btn)
        bosses_view.add_item(self.down_btn)
        bosses_view.add_item(self.detail)
        bosses_view.add_item(self.add_item_btn)
        return bosses_view


view_builder = ViewBuilder()
