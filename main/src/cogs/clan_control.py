import time
import discord
import datetime

from discord import Embed
from discord.ext import commands, tasks
from discord.commands import Option, slash_command, permissions
from discord.ui import Button

from cogs.base import BaseCog
from config import CLANS_ROLES, ClANS_GUILD_ID, CLANS, USER_ID
from embeds.def_embed import DefaultEmbed
from systems.control_system import control_system


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

    @tasks.loop(minutes=60)
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

        async def start_callback(interaction: discord.Interaction):
            check_member_to_work, time_check = control_system.find_clan_control_is_working(interaction.user.id)
            find_clan_control_on_base = control_system.find_clan_control_on_base(member_id=interaction.user.id)
            sec_end_check = int(time.time()) - time_check
            ty_res = time.gmtime(sec_end_check)
            res = time.strftime("%H:%M:%S", ty_res)
            if int(res) >= 10:
                return await interaction.response.send_message(embed=DefaultEmbed('***```Вы опоздали с проверкой, возьмете следуйщую```***'), ephemeral=True)
            if interaction.user.id != find_clan_control_on_base:
                return await interaction.response.send_message(embed=DefaultEmbed('***```Ты не клан контрол((((```***'), ephemeral=True)

            if check_member_to_work is True:
                return await interaction.response.send_message(embed=DefaultEmbed('***```Ты не закончил прошлую проверку```***'), ephemeral=True)

            for i in interaction.user.roles:

                if i == self.clan_control:
                    _accept = Embed(title='Проверка на афк', description=f'***```Не забудь сдать провепку в конце.```***', color=0x292b2f)
                    _accept.add_field(name='Время принятия:', value=f'<t:{self.create_time}>')
                    _accept.add_field(name='Кто проводит:', value=interaction.user.mention, inline=True)
                    button_start.disabled = True
                    control_system.start_to_word(member_id=interaction.user.id, time_check=self.create_time)
                    return await msg.edit(embed=_accept, view=view)

        async def finish_callback(interaction: discord.Interaction):
            check_member_to_work, time_check = control_system.find_clan_control_is_working(interaction.user.id)
            find_clan_control_on_base = control_system.find_clan_control_on_base(member_id=interaction.user.id)
            sec_end_check = int(time.time()) - time_check
            ty_res = time.gmtime(sec_end_check)
            res = time.strftime("%H:%M:%S", ty_res)
            if interaction.user.id != find_clan_control_on_base:
                return await interaction.response.send_message(embed=DefaultEmbed('***```Ты не клан контрол((((```***'), ephemeral=True)

            if check_member_to_work is False:
                return await interaction.response.send_message(embed=DefaultEmbed('***```Ты не взял проверку челлл```***'), ephemeral=True)

            for i in interaction.user.roles:
                if i == self.clan_control:
                    _decline = Embed(title='Проверка на афк', description=f'***```Проверка была завершена успешно.```***')
                    _decline.add_field(name='Время проверки', value=res)
                    _decline.add_field(name='Время окончания:', value=f'<t:{self.create_time}>')
                    _decline.add_field(name='Кто проводил:', value=interaction.user.mention, inline=False)
                    button_finish.disabled = True
                    control_system.return_to_work(member_id=interaction.user.id)
                    return await msg.edit(embed=_decline, view=view)

        button_start.callback = start_callback
        button_finish.callback = finish_callback

    @slash_command(name='cc_add', description='enter member to add', guild_ids=[ClANS_GUILD_ID], default_permission=False)
    @permissions.permission(user_id=USER_ID, permission=True)
    async def cc_add(self, ctx, member: Option(discord.Member, 'enter the member', required=True)):
        check_member_for_a_base = control_system.find_clan_control_on_base(member_id=member.id)
        if member.id == check_member_for_a_base:
            return await ctx.respond(embed=DefaultEmbed(f'***```{member.name} вже є клан контролом```***'))

        control_system.add_new_clan_control(member_id=member.id, control_role=CLANS_ROLES['CLAN_CONTROL_ROLE_ID'], add_time=self.create_time)
        return await ctx.respond(embed=DefaultEmbed(f'***```{member.name} був прийнятий на клан контрола```***'))

    @slash_command(name='cc_kick', description='enter member to kick', guild_ids=[ClANS_GUILD_ID], default_permission=False)
    @permissions.permission(user_id=USER_ID, permission=True)
    async def cc_kick(self, ctx, member: Option(discord.Member, 'enter the member', required=True)):
        check_member_for_a_base = control_system.find_clan_control_on_base(member_id=member.id)

        if member.id != check_member_for_a_base:
            return await ctx.respond(embed=DefaultEmbed(f'***```{member.name} не клан контрол```***'))

        control_system.kick_clan_control(member_id=member.id)
        return await ctx.respond(embed=DefaultEmbed(f'***```{member.name} був знятий з клан контрола```***'))

    @slash_command(name='cc_list', description='Список клан контролов', guild_ids=[ClANS_GUILD_ID], default_permission=False)
    @permissions.permission(user_id=USER_ID, permission=True)
    async def cc_list(self, ctx):
        counter = 1
        description = f'***```Все клан контролы:```***\n'
        member = control_system.enumeration_clan_control(CLANS_ROLES['CLAN_CONTROL_ROLE_ID'])
        for i in member:
            get_member = ctx.guild.get_member(i['member_id'])
            description += f'{counter} - {get_member.mention} - {str(i["check_num"])} - <t:{i["time_add"]}>' + '\n'
            counter += 1
        return await ctx.respond(embed=DefaultEmbed(f'{description}'))

    @slash_command(name='cc_clear', description='Обнуление проверок всех клан контролов', guild_ids=[ClANS_GUILD_ID], default_permission=False)
    @permissions.permission(user_id=USER_ID, permission=True)
    async def cc_clear(self, ctx):
        control_system.clear_check(CLANS_ROLES['CLAN_CONTROL_ROLE_ID'])
        return await ctx.respond(embed=DefaultEmbed('***```Вы очистили проверки контролов.```***'))


def setup(client):
    client.add_cog(ClanControl(client))
    print("Cog 'clan control' connected!")
