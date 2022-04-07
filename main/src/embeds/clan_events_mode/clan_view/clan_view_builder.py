import discord
from discord.ui import View, Button


class ClanViewBuilder:
    def __init__(self):
        self.settings_manu_invite = Button(style=discord.ButtonStyle.green, label='Invite')
        self.settings_manu_kick = Button(style=discord.ButtonStyle.green, label='Kick')
        self.settings_manu_up_to_zam = Button(style=discord.ButtonStyle.secondary, label='Up to zam')
        self.settings_manu_remove_zam = Button(style=discord.ButtonStyle.secondary, label='Remove zam')

        self.button_accept_delete = Button(style=discord.ButtonStyle.green, label='Accept')
        self.button_decline_delete = Button(style=discord.ButtonStyle.red, label='Decline')

        self.button_invite_clan_accept = Button(style=discord.ButtonStyle.green, label='Accept')
        self.button_invite_clan_decline = Button(style=discord.ButtonStyle.red, label='Decline')

    def delete_clan_view(self) -> View:
        delete_view = View(timeout=None)
        delete_view.add_item(self.button_accept_delete)
        delete_view.add_item(self.button_decline_delete)
        return delete_view

    def invite_clan_view(self) -> View:
        invite_view = View(timeout=None)
        invite_view.add_item(self.button_invite_clan_accept)
        invite_view.add_item(self.button_invite_clan_decline)
        return invite_view

    def setting__clan_menu(self) -> View:
        settings_menu = View(timeout=None)
        settings_menu.add_item(self.settings_manu_invite)
        settings_menu.add_item(self.settings_manu_kick)
        settings_menu.add_item(self.settings_manu_up_to_zam)
        settings_menu.add_item(self.settings_manu_remove_zam)
        return settings_menu


clan_view_builder = ClanViewBuilder()
