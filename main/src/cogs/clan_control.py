import datetime
import time
from datetime import date

import discord
from discord import Embed
from discord.commands import permissions, slash_command
from discord.ext import commands, tasks
from discord.ui import Button
from discord.ui import Select

from cogs.base import BaseCog
from config import CLANS_ROLES, ClANS_GUILD_ID, BladeXses, PREFIX, Less, LOG_CHAT, CURATOR_ROLE, \
    CLANS_CONTROL_CHAT
from embeds.def_embed import DefaultEmbed
from systems.clan_staff.control_system import control_system

desire_bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())


def time_converter(server_name: str):
    validity_check = control_system.check_validity(server_name=server_name)
    ty_res = time.gmtime(int(time.time()) - int(validity_check))
    return str(time.strftime("%M:%S", ty_res))


def end_work(member_id: int):
    time_check = control_system.get_time_check(member_id=member_id)
    time_work = time.gmtime(int(time.time()) - int(time_check))
    return str(time.strftime("%M:%S", time_work))


class ClanControl(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        print("Cog 'clan control' connected!")
        self.log_chat = None
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

        self.clan_chat = self.client.get_channel(CLANS_CONTROL_CHAT)
        self.log_chat = self.client.get_channel(LOG_CHAT)

        if not self.clan_chat:
            print('Cannot find CLANS_CONTROL_CHAT in guild')
            await self.client.close()

        self.clan_control = discord.utils.get(self.guild.roles, id=CLANS_ROLES['CLAN_CONTROL_ROLE_ID'])
        self.create_time = int(time.time())

    @commands.command(name='start_checks')
    async def start_checks(self, ctx):
        await ctx.channel.purge(limit=1)
        if ctx.message.author.id != 450361269128790026:
            return await ctx.send('...')
        else:
            if not self.check_for_afk.is_running():
                self.check_for_afk.start()
                return await ctx.send('***```Перевірки було успішно запущено.```***')

            if self.check_for_afk.is_running():
                self.check_for_afk.cancel()
                return await ctx.send('***```Перевірки було успішно призупинено.```***')

    @tasks.loop(minutes=60)
    async def check_for_afk(self):
        control_system.remove_time_old_check(server_name='Tenderly')

        button_start = Button(style=discord.ButtonStyle.secondary, label='Взять', emoji='❕')
        button_finish = Button(style=discord.ButtonStyle.secondary, label='Сдать', emoji='❗')
        button_url = Button(style=discord.ButtonStyle.url, label='Таблица', url=self.url)

        view = discord.ui.View(timeout=None)
        view.add_item(button_start)
        view.add_item(button_finish)
        view.add_item(button_url)

        control_system.time_start_checks_embed(int(time.time()))

        _embed = Embed(title='Перевірка на афк', description=f'***```Наступив час проводити перевірку...```***')
        _embed.add_field(name='Час:', value=f'<t:{int(time.time())}>')
        _embed.add_field(name='Роботяги:', value=f'{self.clan_control.mention}', inline=True)
        msg = await self.clan_chat.send(embed=_embed, view=view)

        async def start_callback(ctx):
            find_clan_control_on_base = control_system.find_clan_control_on_base(member_id=ctx.user.id)

            if ctx.user.id != find_clan_control_on_base:
                return await ctx.response.send_message(embed=DefaultEmbed('***```Уви, но ти не клан контрол```***'), ephemeral=True)

            try:
                if time_converter(server_name="Tenderly") >= '15:00':
                    control_system.remove_time_old_check(server_name='Tenderly')
                    return await ctx.response.send_message(embed=DefaultEmbed('***```Вы опоздали, берите следующую проверку!```***'), ephemeral=True)
            except TypeError:
                return await ctx.response.send_message(embed=DefaultEmbed('***```Вы опоздали, берите следующую проверку!```***'), ephemeral=True)

            check_queue = control_system.check_queue(member_id=ctx.user.id)
            if int(check_queue) >= 2:
                return await ctx.response.send_message(embed=DefaultEmbed('***```Нельзя взять больше 2 проверок подряд!```***'), ephemeral=True)

            check_member_to_work = control_system.find_clan_control_is_working(ctx.user.id)
            if check_member_to_work is True:
                return await ctx.response.send_message(embed=DefaultEmbed('***```Ти не закінчив попередню перевірку```***'), ephemeral=True)

            control_system.update_queue(member_id=ctx.user.id, control_role_id=CLANS_ROLES['CLAN_CONTROL_ROLE_ID'])
            _accept = Embed(title='Перевірка на афк', description=f'***```Не забудьте здати перевірку в кінці...```***', color=ctx.user.color)
            _accept.add_field(name='Час прийняття:', value=f'<t:{int(time.time())}>')
            _accept.add_field(name='Хто проводив:', value=ctx.user.mention, inline=True)
            _accept.set_thumbnail(url='https://static.wixstatic.com/media/6e794f_f64d7ba6be8641dbb8b91587bfe23b07~mv2.gif')
            button_start.disabled = True
            control_system.start_to_word(member_id=ctx.user.id, time_check=int(time.time()), today=date.today().isoweekday())
            return await msg.edit(embed=_accept, view=view)

        async def finish_callback(ctx):
            find_clan_control_on_base = control_system.find_clan_control_on_base(member_id=ctx.user.id)

            if ctx.user.id != find_clan_control_on_base:
                return await ctx.response.send_message(embed=DefaultEmbed('***```Уви, но ти не клан контрол```***'), ephemeral=True)

            check_member_to_work = control_system.find_clan_control_is_working(ctx.user.id)
            if check_member_to_work is False:
                return await ctx.response.send_message(embed=DefaultEmbed('***```Спочатку візьми перевірку.```***'), ephemeral=True)

            check_num = control_system.get_clan_control_check_num(ctx.user.id)
            _decline = Embed(title='Перевірка на афк', description=f'***```Перевірка була завершена успішно!```***', color=ctx.user.color)
            _decline.add_field(name='Часу потрачено', value=end_work(member_id=ctx.user.id))
            _decline.add_field(name='Час закінчення:', value=f'<t:{int(time.time())}>')
            _decline.add_field(name='Хто проводив:', value=ctx.user.mention, inline=False)
            _decline.set_footer(text=f'{ctx.user.name}, всього перевірок за тиждень: {str(check_num)}')
            _decline.set_thumbnail(url='https://static.wixstatic.com/media/6e794f_f64d7ba6be8641dbb8b91587bfe23b07~mv2.gif')
            button_finish.disabled = True
            control_system.return_to_work(member_id=ctx.user.id)
            control_system.remove_time_old_check(server_name='Tenderly')
            return await msg.edit(embed=_decline, view=view)

        button_start.callback = start_callback
        button_finish.callback = finish_callback

    @commands.command(name='cc_add')
    @commands.has_role(item=CURATOR_ROLE)
    async def cc_add(self, ctx, member: discord.Member):
        author = ctx.author.id

        match author:
            case 450361269128790026 | 714988384325730306 | 450361269128790026 as author:
                check_member_for_a_base = control_system.find_clan_control_on_base(member_id=member.id)

                if member is ctx.author:
                    return await ctx.send(embed=DefaultEmbed(f'***```Нельзя использовать на себя.```***'))
                if member.id == check_member_for_a_base:
                    return await ctx.send(embed=DefaultEmbed(f'***```{member.name} вже є клан контролом```***'))

                control_system.add_new_clan_control(member_id=member.id, control_role=CLANS_ROLES['CLAN_CONTROL_ROLE_ID'],
                                                    add_time=int(time.time()))
                control_system.add_week_day_clan_control(member_id=member.id, control_role=CLANS_ROLES['CLAN_CONTROL_ROLE_ID'],
                                                         member_name=member.name)
                return await ctx.send(embed=DefaultEmbed(f'***```{member.name} був прийнятий на клан контрола```***'))

    @commands.command(name='cc_kick')
    @commands.has_role(item=CURATOR_ROLE)
    async def cc_kick(self, ctx, member: discord.Member):
        author = ctx.author.id

        match author:
            case 450361269128790026 | 714988384325730306 | 450361269128790026 as author:

                check_member_for_a_base = control_system.find_clan_control_on_base(member_id=member.id)

                if member is ctx.author:
                    return await ctx.send(embed=DefaultEmbed(f'***```Нельзя использовать на себя.```***'))
                if member.id != check_member_for_a_base:
                    return await ctx.send(embed=DefaultEmbed(f'***```{member.name} не клан контрол.```***'))

                control_system.kick_clan_control(member_id=member.id)
                return await ctx.send(embed=DefaultEmbed(f'***```{member.name} був знятий з клан контрола```***'))

    @commands.command(name='cc_list')
    @commands.has_role(item=CLANS_ROLES['CLAN_CONTROL_ROLE_ID'])
    async def cc_list(self, ctx):

        counter = 1
        description = f'***```Все клан контролы:```***\n'
        member = control_system.enumeration_clan_control(CLANS_ROLES['CLAN_CONTROL_ROLE_ID'])
        for i in member:
            get_member = ctx.guild.get_member(i['member_id']).mention
            description += f'{counter} - {get_member} - {str(i["check_num"])} - <t:{i["time_add"]}>' + '\n'
            counter += 1
        return await ctx.send(embed=DefaultEmbed(f'{description}'))

    @commands.command(name='cc_clear')
    @commands.has_role(item=CURATOR_ROLE)
    async def cc_clear(self, interaction: discord.Interaction):
        print(interaction.user, 'use command cc_clear to at', int(time.time()))

        control_system.clear_check(CLANS_ROLES['CLAN_CONTROL_ROLE_ID'])
        return await interaction.response.send_message(
            embed=DefaultEmbed('***```Вы очистили проверки контролов.```***'))

    @slash_command(name='cc_week', description='get check clan controls for the week', guild_ids=[ClANS_GUILD_ID],
                   default_permission=False)
    @permissions.has_role(CLANS_ROLES['CLAN_CONTROL_ROLE_NAME'])
    @permissions.permission(user_id=BladeXses)
    @permissions.permission(user_id=Less)
    async def cc_week(self, inter: discord.Interaction):

        controllers_options = []

        for i in control_system.find_all_clan_controllers_ids(CLANS_ROLES['CLAN_CONTROL_ROLE_ID']):
            member = inter.guild.get_member(i["member_id"]).name
            controllers_options.append(discord.SelectOption(label=member, description=i['all_day'], emoji='✔'))

        drop_down_menu = Select(options=controllers_options, placeholder='Виберіть контрола для відображення')

        view = discord.ui.View()
        view.add_item(drop_down_menu)

        await inter.response.send_message('***```Select clan control:```***', view=view, ephemeral=True)

        async def menu_callback(interaction: discord.Interaction):
            member_id, one, two, three, four, five, six, seven, all_day = control_system.view_checks_for_the_week(drop_down_menu.values[0])
            get_member = interaction.guild.get_member(member_id)
            _week_embed = Embed(title='Проверки за неделю',
                                description=f'**Користувач:**{get_member.mention}')
            _week_embed.add_field(name='Пн:', value=one, inline=True)
            _week_embed.add_field(name='Вт:', value=two, inline=True)
            _week_embed.add_field(name='Ср:', value=three, inline=True)
            _week_embed.add_field(name='Чт:', value=four, inline=True)
            _week_embed.add_field(name='Пт:', value=five, inline=True)
            _week_embed.add_field(name='Сб:', value=six, inline=True)
            _week_embed.add_field(name='Нд:', value=seven, inline=True)
            _week_embed.set_footer(text=f'Всього:{str(all_day)}',
                                   icon_url='https://tenor.com/view/cute-cute-cat-cat-dance-dance-danse-gif-17603476')
            await interaction.response.edit_message(embed=_week_embed, view=view)

        drop_down_menu.callback = menu_callback


def setup(bot):
    bot.add_cog(ClanControl(bot))
