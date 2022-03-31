import time

import discord
from discord.commands import slash_command, Option
from discord.ext import commands
from discord.ui import Button
from enun_clan_events_list.event_list import EnumEventList
from embeds.clan_events_mode.request_event_embed import RequestEmbed
from embeds.clan_events_mode.request_accept import RequestAcceptEmbed
from embeds.clan_events_mode.request_pass import RequestPassEmbed
from embeds.clan_events_mode.request_decline import RequestDeclineEmbed
from cogs.base import BaseCog
from config import ClANS_GUILD_ID, LOG_CHAT, CLANS_EVENT_CHAT, CLAN_VOICE_CATEGORY_NAME, CLANS_ROLES, CURATOR_ROLE, Razefuin
from embeds.def_embed import DefaultEmbed
from systems.clan_staff.events_system import events_system


def sum_time_event(message_id: int):
    time_check = events_system.get_time_create_event(message_id=message_id)
    time_work = time.gmtime(int(time.time()) - int(time_check))
    return str(time.strftime("%H:%M:%S", time_work))


def wasting_time_in_seconds(message_id: int):
    time_check = events_system.get_time_create_event(message_id=message_id)
    return time.gmtime(int(time.time()) - int(time_check))


class EventsMode(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        self.guild = None
        self.log_chat = None
        self.client = client
        self.clan_event_chat = None
        self.clan_control_role = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.client.get_guild(ClANS_GUILD_ID)

        self.clan_control_role = discord.utils.get(self.guild.roles, id=CLANS_ROLES['CLAN_CONTROL_ROLE_ID'])

        self.clan_event_chat = self.client.get_channel(CLANS_EVENT_CHAT)
        self.log_chat = self.client.get_channel(LOG_CHAT)

        if not self.clan_event_chat:
            print('Cannot find CLANS_EVENT_CHAT in guild')
            await self.client.close()

    @commands.command(name='add_event')
    # @commands.has_role(item=CURATOR_ROLE)
    async def add_event(self, ctx, member: discord.Member):
        if member is None:
            return await ctx.send(embed=DefaultEmbed(f'***```Вы не указали пользователя.```***'))
        if member is ctx.author:
            return await ctx.send(embed=DefaultEmbed(f'***```Нельзя использовать на себя.```***'))
        author = ctx.author.id

        match author:
            case 450361269128790026 | 714988384325730306 | 450361269128790026 as author:
                check_member_for_a_base = events_system.find_clan_events_mode_on_base(member_id=member.id)
                if member.id == check_member_for_a_base:
                    return await ctx.send(embed=DefaultEmbed(f'***```{member.name} вже є клан контролом```***'))

                events_system.add_new_clan_events_mode(control_role_id=CLANS_ROLES['CLAN_CONTROL_ROLE_ID'], member_id=member.id, add_time=int(time.time()))
                return await ctx.send(embed=DefaultEmbed(f'***```{member.name}, был добавлен к списку клан ивентеров.```***'))

    @commands.command(name='kick_event')
    @commands.has_role(item=CURATOR_ROLE)
    async def kick_event(self, ctx, member: discord.Member):
        author = ctx.author.id

        match author:
            case 450361269128790026 | 714988384325730306 | 450361269128790026 as author:
                check_member_for_a_base = events_system.find_clan_events_mode_on_base(member_id=member.id)
                if member.id != check_member_for_a_base:
                    return await ctx.send(embed=DefaultEmbed(f'***```{member.name} не клан контрол.```***'))

                events_system.remove_clan_events_mode(member_id=member.id)
                return await ctx.send(embed=DefaultEmbed(f'***```{member.name}, был успешно удален из списка клан ивентеров.```***'))

    @commands.command(name='events_list')
    @commands.has_role(item=CLANS_ROLES['CLAN_CONTROL_ROLE_ID'])
    async def events_list(self, ctx):
        counter = 1
        description = f'***```Все клан ивентёры:```***\n**№|user|event num|wasting event time| add time|**\n'
        members = events_system.enumeration_events_mode(CLANS_ROLES['CLAN_CONTROL_ROLE_ID'])
        for member in members:
            get_member = ctx.guild.get_member(member['member_id']).mention
            total_time = time.gmtime(member["sum_wasting_time"])
            description += f'{counter} - {get_member} - {str(member["all_sum_events_end"])} - {str(time.strftime("%H:%M:%S", total_time))} - <t:{member["add_time"]}>' + '\n'
            counter += 1
        return await ctx.send(embed=DefaultEmbed(f'{description}'))

    @slash_command(name='event_request', description='Select the event', guild_ids=[ClANS_GUILD_ID], default_permission=True)
    # @commands.cooldown(1, 60, commands.BucketType.member)
    async def event_request(self, interaction: discord.Interaction, event_list: Option(str, 'chose item', choices=EnumEventList.list(), required=True)):
        button_accept = Button(style=discord.ButtonStyle.secondary, label='Взять ивент', emoji='❕')
        button_end = Button(style=discord.ButtonStyle.secondary, label='Сдать ивент', emoji='❗')
        button_decline = Button(style=discord.ButtonStyle.secondary, label='Отказ от ивента', emoji='❌')

        view = discord.ui.View(timeout=None)
        view.add_item(button_accept)
        view.add_item(button_decline)
        members_id = []
        for category in interaction.guild.categories:
            if category.name == CLAN_VOICE_CATEGORY_NAME:
                for channel in category.voice_channels:
                    for member in channel.members:
                        members_id.append(member.id)
        print(members_id)
        if interaction.user.id in members_id:
            request_msg = await self.clan_event_chat.send(
                embed=RequestEmbed(clan_name=str(interaction.user.voice.channel.name), event_name=event_list, interaction=interaction,
                                   members_on_voice=sum([1 for member in str(interaction.user.voice.channel.members)]),
                                   clan_control_role=self.clan_control_role.mention).embed,
                view=view)
            events_system.request_create(message_id=request_msg.id, clan_name=interaction.user.voice.channel.name, event_name=event_list, member_id=interaction.user.id)

            await interaction.response.send_message(
                embed=DefaultEmbed(
                    f'***```{interaction.user.name}, запрос на ивент был успешно отправлен;\nПожалуйста дождитесь ответа ивентера.```***'),
                ephemeral=True)

            async def accept_callback(ctx):

                find_clan_events_mode_on_base = events_system.find_clan_events_mode_on_base(member_id=ctx.user.id)

                if ctx.user.id != find_clan_events_mode_on_base:
                    return await ctx.response.send_message(embed=DefaultEmbed('***```Уви, но ти не клан ивентер```***'), ephemeral=True)

                check_member_to_work = events_system.find_clan_event_mode_is_working(member_id=ctx.user.id)
                if check_member_to_work is True:
                    return await ctx.response.send_message(embed=DefaultEmbed('***```Ты уже проводишь ивент.```***'), ephemeral=True)

                clan_name, event_name, member_create_request = events_system.get_request(message_id=request_msg.id)
                events_system.accept_request(request_msg.id, ctx.user.id)
                get_member = ctx.guild.get_member(member_create_request).name
                view.add_item(button_end)
                view.remove_item(button_accept)
                view.remove_item(button_decline)
                await interaction.user.send(embed=DefaultEmbed(f'***```{ctx.user.name}, принял запрос ивента;\nОжидайте в ближайшее время.```***'))
                await request_msg.edit(
                    embed=RequestAcceptEmbed(clan_name=clan_name, event_name=event_name, create_request_member=get_member,
                                             clan_control=ctx.user.name).embed,
                    view=view)

            async def decline_callback(ctx):
                view.remove_item(button_accept)
                view.remove_item(button_decline)
                if ctx.user.id != Razefuin:
                    return await ctx.response.send_message(embed=DefaultEmbed('***```Извинись, и на колени```***'), ephemeral=True)

                view.remove_item(button_accept)
                clan_name, event_name, member_create_request = events_system.get_request(message_id=request_msg.id)
                get_member = ctx.guild.get_member(member_create_request).name
                events_system.request_delete(request_msg.id)
                await interaction.user.send(embed=DefaultEmbed(f'***```{ctx.user.name}, отклонил запрос на проведение ивента```***'))
                await request_msg.edit(
                    embed=RequestDeclineEmbed(clan_name=clan_name, event_name=event_name, create_request_member=get_member, curator=ctx.user.name).embed,
                    view=view)

            async def pass_callback(ctx):
                check_request_id = events_system.checks_event_mode_to_work(member_id=ctx.user.id)

                if check_request_id is None:
                    return await ctx.send_message(f'{ctx.user.name}, это не ваш ивент.')

                if check_request_id != request_msg.id:
                    return await ctx.send_message(f'{ctx.user.name}, это не ваш ивент.')

                view.remove_item(button_end)
                view.remove_item(button_decline)
                clan_name, event_name, member_create_request = events_system.get_request(message_id=request_msg.id)
                get_member = ctx.guild.get_member(member_create_request).name
                sum_time_event(message_id=request_msg.id)
                time_check = events_system.get_time_create_event(message_id=request_msg.id)
                events_system.adding_event_data_to_events_mode(member_id=ctx.user.id, waisting_time=int(time.time()) - int(time_check))
                await request_msg.edit(
                    embed=RequestPassEmbed(clan_name=clan_name, event_name=event_name, create_request_member=get_member,
                                           clan_control=ctx.user.name, event_pass=sum_time_event(request_msg.id)).embed, view=view)
                events_system.request_delete(message_id=request_msg.id)
                events_system.submit_request(member_id=ctx.user.id)

            button_accept.callback = accept_callback
            button_end.callback = pass_callback
            button_decline.callback = decline_callback
        else:
            return await interaction.response.send_message(embed=DefaultEmbed(f'***```Вы должны быть в войсе клана.```***'))


def setup(client):
    client.add_cog(EventsMode(client))
    print("Cog 'clan event' connected!")
