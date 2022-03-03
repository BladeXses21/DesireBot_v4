import time
import discord
import datetime

from discord import Colour, Embed
from discord.ext import commands, tasks
from discord.utils import get
from discord.commands import Option, slash_command
from discord.ui import Button

from cogs.base import BaseCog
from config import CLANS_ROLES, ClANS_GUILD_ID, CLANS
from embeds.def_embed import DefaultEmbed


class ClanControl(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        self.client = client
        self.clan_control = None
        self.guild = None
        self.clan_chat = None
        self.everyone_role = None
        self.create_time = None
        self.time_now = datetime.datetime.now()
        self.url = 'https://docs.google.com/spreadsheets/d/1lWEL6Iw3j0HXJgS54eMHE0zat-uMBiIkBHwvHAuqdFA/edit#gid=0'

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.client.get_guild(ClANS_GUILD_ID)

        self.clan_chat = self.client.get_channel(CLANS['CLAN_CHAT'])

        if not self.clan_chat:
            print('Cannot find CLANS_CATEGORY in guild')
            await self.client.close()

        self.clan_control = discord.utils.get(self.guild.roles, id=CLANS_ROLES['CLAN_CONTROL_ROLE_ID'])
        self.everyone_role = discord.utils.get(self.guild.roles, name="@everyone")
        self.create_time = int(time.time())

        self.check_for_afk.start()

    @tasks.loop(seconds=500)
    async def check_for_afk(self):

        button_start = Button(style=discord.ButtonStyle.secondary, label='Взять', emoji='❕')
        button_finish = Button(style=discord.ButtonStyle.secondary, label='Сдать', emoji='❗')
        button_url = Button(style=discord.ButtonStyle.url, label='Таблица', url=self.url)

        view = discord.ui.View()
        view.add_item(button_start)
        view.add_item(button_finish)
        view.add_item(button_url)

        _embed = Embed(title='Проверка на афк', description=f'***```Пришло время проводить проверку!```***')
        _embed.add_field(name='Время:', value=f'<t:{self.create_time}>')
        _embed.add_field(name='Ребята:', value=f'{self.clan_control.mention}', inline=True)

        msg = await self.clan_chat.send(embed=_embed, view=view)

        async def StartCallback(interaction: discord.Interaction):
            for i in interaction.user.roles:
                if i == self.clan_control:
                    _accept = Embed(title='Проверка на афк', description=f'***```Не забудь сдать провепку в конце.```***')
                    _accept.add_field(name='Время принятия:', value=f'<t:{self.create_time}>')
                    _accept.add_field(name='Кто проводит:', value=interaction.user.mention, inline=True)
                    button_start.disabled = True
                    return await msg.edit(embed=_accept, view=view)

        async def FinishCallback(interaction: discord.Interaction):
            for i in interaction.user.roles:
                if i == self.clan_control:
                    _decline = Embed(title='Проверка на афк', description=f'***```Проверка была завершена успешно.```***')
                    _decline.add_field(name='Время окончания:', value=f'<t:{self.create_time}>')
                    _decline.add_field(name='Кто проводил:', value=interaction.user.mention, inline=True)
                    button_finish.disabled = True
                    return await msg.edit(embed=_decline, view=view)

        button_start.callback = StartCallback
        button_finish.callback = FinishCallback


# todo - сделать проверку через базу данных и сделать отключение кнопок при нажатии

def setup(client):
    client.add_cog(ClanControl(client))
    print("Cog 'clan control' connected!")
