import discord
from discord.ui import View, Button


class ViewBuilder:
    def __init__(self):
        self.button_attack = Button(style=discord.ButtonStyle.green, label='Attack', emoji="<:933511914707906590:960339513765429278>")
        self.button_profile = Button(style=discord.ButtonStyle.blurple, label='Profile', emoji="<:933511914384920577:960339396350050406>")

        self.button_inventory = Button(style=discord.ButtonStyle.secondary, label='Inventory', emoji='<:premiumiconbackpack4672563:960536938631270450>')
        self.button_stats = Button(style=discord.ButtonStyle.secondary, label='Stats', emoji='💎')
        self.button_back = Button(style=discord.ButtonStyle.blurple, label='Back', emoji='<:freeicon3dforwardarrow64844remov:960538574250471424>')

        self.up_inventory_btn = Button(style=discord.ButtonStyle.secondary, emoji='<:freeicon3duparrow64766:960536939138789396>')
        self.down_inventory_btn = Button(style=discord.ButtonStyle.secondary, emoji='<:freeicon3duparrow64766:960539212300562483>')
        self.equip_btn = Button(style=discord.ButtonStyle.green, emoji='<:icons896:960344174551502858>')

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
