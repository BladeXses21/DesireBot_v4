from discord import ButtonStyle
from discord.ui import Button


class Buttons:
    def __init__(self):
        self.back_btn = Button(style=ButtonStyle.secondary, label='', emoji='🔙')

        self.attack_btn = Button(style=ButtonStyle.green, label='Attack', emoji="🗡")
        self.profile_btn = Button(style=ButtonStyle.blurple, label='Profile', emoji="📖")

        self.inventory_btn = Button(style=ButtonStyle.secondary, label='Inventory', emoji='🧳')

        self.up_btn = Button(style=ButtonStyle.secondary, label='', emoji='⬆')
        self.down_btn = Button(style=ButtonStyle.secondary, label='', emoji='⬇')
        self.equip_btn = Button(style=ButtonStyle.green, label='Equip')

        self.choose_btn = Button(style=ButtonStyle.blurple, label='Choose')
        self.add_items_btn = Button(style=ButtonStyle.secondary, label='Add items')
        self.delete_btn = Button(style=ButtonStyle.red, label='Delete')

        self.detail_btn = Button(style=ButtonStyle.secondary, label='', emoji='ℹ')
        self.add_item_btn = Button(style=ButtonStyle.blurple, label='', emoji='➕')
        self.remove_item_btn = Button(style=ButtonStyle.red, label='', emoji='➖')

        self.enemies_btn = Button(style=ButtonStyle.secondary, label='Enemies')
        self.items_btn = Button(style=ButtonStyle.secondary, label='Items')
        self.heroes_btn = Button(style=ButtonStyle.secondary, label='Heroes')


buttons = Buttons()
