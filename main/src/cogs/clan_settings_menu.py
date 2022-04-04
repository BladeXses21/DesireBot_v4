import discord
from discord.ext import commands
from discord.ui import View, Button
from main import client
from cogs.base import BaseCog
from embeds.clans_setting_menu.settings_menu_embed import SettingsMenu
from config import CLAN_SETTING_CHAT
from embeds.def_embed import DefaultEmbed


class ClanSettingsMenu(BaseCog):

    def __init__(self, client):
        super().__init__(client)
        self.client = client
        self.channel = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.client.get_channel(CLAN_SETTING_CHAT)

        # await self.menu_setting()

    async def menu_setting(self):
        button_invite = Button(style=discord.ButtonStyle.green, label='Accept')
        button_kick = Button(style=discord.ButtonStyle.green, label='Kick')

        view = discord.ui.View(timeout=None)
        view.add_item(button_invite)
        view.add_item(button_kick)
        await self.channel.send(embed=SettingsMenu().embed, view=view)

        async def invite_callback(ctx):
            await ctx.response.send_message('invite')

        button_invite.callback = invite_callback


def setup(client):
    client.add_cog(ClanSettingsMenu(client))
    print("Cog 'clan setting menu' connected!")
