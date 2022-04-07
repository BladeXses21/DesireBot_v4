import time

from discord import Embed
from discord.ui import Select

from cogs.base import BaseCog
import discord
from discord.commands import permissions, slash_command, Option
from discord.ext import commands

from config import ClANS_GUILD_ID, CLAN_VOICE_CATEGORY_NAME, CLANS_ROLES, BladeXses, CLANS_EVENT_CHAT, CLAN_TEXT_CATEGORY_NAME, CLANS, CURATOR_ROLE
from embeds.clan_events_mode.close_embeds.accept_close_embed import AcceptCloseEmbed
from embeds.clan_events_mode.close_embeds.accept_close_from_events_mode import AcceptCloseFromEventMode
from embeds.clan_events_mode.close_embeds.close_request_embed import CloseRequestEmbed
from embeds.clan_events_mode.close_embeds.decline_close_embed import DeclineResponseCloseEmbed, DeclineCloseEmbed
from embeds.clan_events_mode.close_embeds.who_win import WinCloseFromEventMode
from embeds.clan_events_mode.clan_view.close_request_view_builder import close_request_view_builder
from embeds.def_embed import DefaultEmbed
from embeds.clan_events_mode.enun_clan_events_list.close_event_list import EnumCloseEventList
from systems.clan_staff.clan_close_rating_system import clan_rating_system
from systems.clan_staff.close_event_system import close_event_system
from systems.clan_staff.events_system import events_system


def clan_text_channel_list(interaction: discord.Interaction) -> list:
    clans_channels_list = []
    for category in interaction.guild.categories:
        if category.name == CLAN_TEXT_CATEGORY_NAME:
            for channel in category.text_channels:
                clans_channels_list.append(channel.name)
    return clans_channels_list


def clan_voice_channel_list(interaction: discord.Interaction) -> list:
    members_id = []
    for category in interaction.guild.categories:
        if category.name == CLAN_VOICE_CATEGORY_NAME:
            for channel in category.voice_channels:
                for member in channel.members:
                    members_id.append(member.id)
    return members_id


def sum_time_close_event(message_id: int):
    time_check = close_event_system.get_time_send_request(message_id=message_id)
    time_work_on_seconds = time.gmtime(int(time.time()) - int(time_check))
    return str(time.strftime("%H:%M:%S", time_work_on_seconds))


class CloseRequest(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        self.guild = None
        self.client = client
        self.clan_event_chat = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.client.get_guild(ClANS_GUILD_ID)

        self.clan_event_chat = self.client.get_channel(CLANS_EVENT_CHAT)

        if not self.clan_event_chat:
            print('Cannot find CLANS_EVENT_CHAT in guild')
            await self.client.close()

    @slash_command(name='close_request', description='Вызвать клан на клоз, пропишите команду cc.clan_channel , чтобы узнать действующие кланы',
                   guild_ids=[ClANS_GUILD_ID], default_permission=True)
    async def close_request(self, interaction: discord.Interaction, clan: discord.TextChannel,
                            event: Option(str, 'Выберите ивент', choices=EnumCloseEventList.list(), required=True),
                            users: Option(int, 'Сколько у вас людей?', required=True),
                            comment: Option(str, 'Оставить коментарий', required=False)):
        text_channel_send_request = interaction.channel

        if comment is None:
            comment = 'No comments...'

        create_close_view = close_request_view_builder.create_close_request_view()

        if users <= 4:
            return await interaction.response.send_message(embed=DefaultEmbed('***```Нужно минимум 5 человек.```***'))

        if clan.name in clan_text_channel_list(interaction):
            if interaction.user.id in clan_voice_channel_list(interaction):

                response_to_a_request = await interaction.response.send_message(
                    embed=DefaultEmbed(f'***```{interaction.user.name}, вы успешно отправили вызов клану {clan}```***'))
                request_in_enemy_clan = await clan.send(
                    embed=CloseRequestEmbed(clan_name=clan.name, event_name=event, interaction=interaction, members_on_voice=users, comment=comment).embed,
                    view=create_close_view)
                close_event_system.create_close_request(member_id=interaction.user.id, clan_send_request=str(interaction.user.voice.channel.name),
                                                        clan_accept_request=clan.name, message_request_id=request_in_enemy_clan.id)

                async def clan_accept_callback(ctx: discord.Interaction):
                    if ctx.user.id in clan_voice_channel_list(ctx):
                        text_channel_accept_request = ctx.channel

                        create_close_view.remove_item(close_request_view_builder.accept_request)
                        create_close_view.remove_item(close_request_view_builder.decline_request)

                        event_mode_view = close_request_view_builder.button_for_events_mode()
                        clan_send_name = str(interaction.user.voice.channel.name)
                        member_send_mention = interaction.user.mention
                        member_accept_request = ctx.user.mention
                        await response_to_a_request.edit_original_message(
                            embed=AcceptCloseEmbed(clan_name_requesting=clan_send_name, clan_name_accepted=clan.name,
                                                   event_name=event, member_request=member_send_mention, member_accepted=member_accept_request, comment=comment).embed)
                        await request_in_enemy_clan.edit(
                            embed=AcceptCloseEmbed(clan_name_requesting=clan_send_name, clan_name_accepted=clan.name,
                                                   event_name=event, member_request=member_send_mention, member_accepted=member_accept_request, comment=comment).embed,
                            view=create_close_view)
                        embed_in_event_chat = await self.clan_event_chat.send(
                            embed=AcceptCloseEmbed(clan_name_requesting=clan_send_name, clan_name_accepted=clan.name,
                                                   event_name=event, member_request=member_send_mention, member_accepted=member_accept_request, comment=comment).embed,
                            view=event_mode_view)
                    else:
                        return await interaction.response.send_message(embed=DefaultEmbed('***```Зайдите в головой канал клана, чтобы принять вызов.```***'),
                                                                       ephemeral=True)

                    async def event_mode_accept_callback(inter: discord.Interaction):

                        find_clan_events_mode_on_base = events_system.find_clan_events_mode_on_base(member_id=inter.user.id)
                        if inter.user.id != find_clan_events_mode_on_base:
                            return await inter.response.send_message(embed=DefaultEmbed('***```Уви, но ти не клан ивентер```***'), ephemeral=True)

                        check_member_to_work = events_system.find_clan_event_mode_is_working(member_id=inter.user.id)
                        if check_member_to_work is True:
                            return await inter.response.send_message(embed=DefaultEmbed('***```Ты уже проводишь ивент.```***'), ephemeral=True)

                        clan_battle_view = close_request_view_builder.who_wining_close(clan_name_one=clan_send_name, clan_name_two=clan.name)
                        close_event_system.accept_close_request(message_request_id=request_in_enemy_clan.id, member_id_accept_request=inter.user.id)
                        try:
                            await interaction.user.send(embed=DefaultEmbed(f'***```{inter.user.name}, принял клоз в вашем клане.```***'))
                            await clan.send(embed=DefaultEmbed(f'***```{inter.user.name}, принял клоз в вашем клане.```***'))
                            await embed_in_event_chat.edit(
                                embed=AcceptCloseFromEventMode(clan_name=clan_send_name, clan_name_two=clan.name, event_name=event, event_mode=inter.user.mention,
                                                               comment=comment, interaction=interaction).embed, view=clan_battle_view)
                        except:
                            await clan.send(embed=DefaultEmbed(f'***```{inter.user.name}, принял клоз в вашем клане.```***'))
                            await embed_in_event_chat.edit(
                                embed=AcceptCloseFromEventMode(clan_name=clan_send_name, clan_name_two=clan.name, event_name=event, event_mode=inter.user.mention,
                                                               comment=comment, interaction=interaction).embed, view=clan_battle_view)

                        async def winning_first_clan_callback(i: discord.Interaction):
                            check_request_id = events_system.checks_event_mode_to_work(member_id=i.user.id)

                            if check_request_id is None:
                                return await i.response.send_message(f'{i.user.name}, это не ваш ивент.')

                            if check_request_id != request_in_enemy_clan.id:
                                return await i.response.send_message(f'{i.user.name}, это не ваш ивент.')

                            clan_battle_view.remove_item(close_request_view_builder.first_clan_victory)
                            clan_battle_view.remove_item(close_request_view_builder.second_clan_victory)
                            # result record on system
                            time_start_close_on_seconds = close_event_system.get_time_send_request(request_in_enemy_clan.id)

                            clan_rating_system.add_clan_to_rating_system(clan_name=text_channel_send_request.name, clan_text_id=text_channel_send_request.id)
                            clan_rating_system.add_clan_to_rating_system(clan_name=text_channel_accept_request.name, clan_text_id=text_channel_accept_request.id)
                            events_system.adding_event_data_to_events_mode(member_id=ctx.user.id, waisting_time=int(time.time()) - int(time_start_close_on_seconds))
                            clan_rating_system.clan_victory_in_the_game(clan_text_id=text_channel_send_request.id,
                                                                        clan_waisting_time=int(time.time()) - int(time_start_close_on_seconds))
                            clan_rating_system.clan_loss_in_the_game(clan_text_id=text_channel_accept_request.id,
                                                                     clan_waisting_time=int(time.time()) - int(time_start_close_on_seconds))
                            # final victory embed
                            await embed_in_event_chat.edit(
                                embed=WinCloseFromEventMode(clan_win=clan_send_name, clan_name_two=clan.name, event_name=event, event_mode=i.user.mention,
                                                            sum_time_event=sum_time_close_event(request_in_enemy_clan.id)).embed,
                                view=clan_battle_view)
                            await text_channel_send_request.send(embed=DefaultEmbed(f'***```Ваш клан победил в клозе и получил 25 рейтинга```***'))
                            events_system.submit_request(inter.user.id)
                            close_event_system.delete_close_request(request_in_enemy_clan.id)

                        async def winning_seconds_clan_callback(i: discord.Interaction):
                            check_request_id = events_system.checks_event_mode_to_work(member_id=i.user.id)

                            if check_request_id is None:
                                return await i.response.send_message(f'{i.user.name}, это не ваш ивент.')

                            if check_request_id != request_in_enemy_clan.id:
                                return await i.response.send_message(f'{i.user.name}, это не ваш ивент.')

                            clan_battle_view.remove_item(close_request_view_builder.first_clan_victory)
                            clan_battle_view.remove_item(close_request_view_builder.second_clan_victory)
                            # result record on system
                            time_start_close_on_seconds = close_event_system.get_time_send_request(request_in_enemy_clan.id)

                            clan_rating_system.add_clan_to_rating_system(clan_text_id=text_channel_send_request.id)
                            clan_rating_system.add_clan_to_rating_system(clan_text_id=text_channel_accept_request.id)
                            clan_rating_system.clan_victory_in_the_game(clan_text_id=text_channel_accept_request.id,
                                                                        clan_waisting_time=int(time.time()) - int(time_start_close_on_seconds))
                            clan_rating_system.clan_loss_in_the_game(clan_text_id=text_channel_send_request.id,
                                                                     clan_waisting_time=int(time.time()) - int(time_start_close_on_seconds))
                            events_system.adding_event_data_to_events_mode(member_id=ctx.user.id, waisting_time=int(time.time()) - int(time_start_close_on_seconds))
                            # final victory embed
                            await embed_in_event_chat.edit(
                                embed=WinCloseFromEventMode(clan_win=clan.name, clan_name_two=clan_send_name, event_name=event, event_mode=i.user.mention,
                                                            sum_time_event=sum_time_close_event(request_in_enemy_clan.id)).embed,
                                view=clan_battle_view)
                            await clan.send(embed=DefaultEmbed(f'***```Ваш клан победил в клозе и получил 25 рейтинга```***'))
                            events_system.submit_request(inter.user.id)
                            close_event_system.delete_close_request(request_in_enemy_clan.id)

                        close_request_view_builder.first_clan_victory.callback = winning_first_clan_callback
                        close_request_view_builder.second_clan_victory.callback = winning_seconds_clan_callback

                    async def event_mode_decline_callback(inter: discord.Interaction):

                        find_clan_events_mode_on_base = events_system.find_clan_events_mode_on_base(member_id=inter.user.id)
                        if inter.user.id != find_clan_events_mode_on_base:
                            return await inter.response.send_message(embed=DefaultEmbed('***```Уви, но ти не клан ивентер```***'), ephemeral=True)
                        close_event_system.delete_close_request(request_in_enemy_clan.id)

                        await clan.send(embed=DefaultEmbed(f'***```{inter.user.name}, отказал в проведении клоза.```***'))

                    close_request_view_builder.event_mode_accept_request.callback = event_mode_accept_callback
                    close_request_view_builder.event_mode_decline_request.callback = event_mode_decline_callback

                async def clan_decline_callback(ctx: discord.Interaction):
                    create_close_view.remove_item(close_request_view_builder.accept_request)
                    create_close_view.remove_item(close_request_view_builder.decline_request)
                    close_event_system.delete_close_request(request_in_enemy_clan.id)
                    await response_to_a_request.edit_original_message(embed=DeclineCloseEmbed(str(ctx.user.voice.channel.name), member_decline=ctx.user.mention).embed)
                    await request_in_enemy_clan.edit(
                        embed=DeclineResponseCloseEmbed(str(interaction.user.voice.channel.name), member_decline=ctx.user.mention).embed)

                close_request_view_builder.accept_request.callback = clan_accept_callback
                close_request_view_builder.decline_request.callback = clan_decline_callback

            else:
                return await interaction.response.send_message(embed=DefaultEmbed('***```Ты не находишься в войсе клана```***'), ephemeral=True)
        else:
            return await interaction.response.send_message(embed=DefaultEmbed('***```Ты указал не клан```***'), ephemeral=True)

    @commands.command(name='clan_channel', description='Посмотреть все каналы кланов')
    async def clan_channel(self, ctx):
        clans_channels_collection = '***```Список всех кланов:```***\n'
        counter = 1
        for category in ctx.guild.categories:
            if category.name == CLAN_TEXT_CATEGORY_NAME:
                for channel in category.text_channels:
                    counter += 1
                    clans_channels_collection += f'**{counter}** - ' + f'{channel.mention}' + '\n'
        return await ctx.send(embed=DefaultEmbed(clans_channels_collection), delete_after=20)

    @commands.command(name='give_rating', description='Выдать рейтинг клану')
    @commands.has_role(item=CLANS_ROLES["CLAN_CONTROL_ROLE_ID"])
    async def give_rating(self, ctx, text_channel_id):
        clan_rating_system.add_clan_to_rating_system(clan_text_id=text_channel_id)
        get_clan_text_channel = self.client.get_channel(text_channel_id)
        clan_rating_system.clan_victory_in_the_game(clan_text_id=text_channel_id, clan_waisting_time=60)
        return await ctx.send(f'***```{get_clan_text_channel.name}, получил свои +25 рейтинга.```***')

    @commands.command(name='take_rating', description='Забрать рейтинг клана')
    @commands.has_role(item=CLANS_ROLES["CLAN_CONTROL_ROLE_ID"])
    async def take_rating(self, ctx, text_channel_id):
        clan_rating_system.add_clan_to_rating_system(clan_text_id=text_channel_id)
        get_clan_text_channel = self.client.get_channel(text_channel_id)
        clan_rating_system.clan_loss_in_the_game(clan_text_id=text_channel_id, clan_waisting_time=60)

        return await ctx.send(f'***```{get_clan_text_channel.name}, рейтинг был снижен на 25.```***')

    @commands.command(name='rem_from_rating', description='Удалить клан с системы рейтинга')
    @commands.has_role(item=CURATOR_ROLE)
    async def rem_from_rating(self, ctx, clan_name):
        clan_rating_system.remove_from_rating(clan_name)
        return await ctx.send(embed=DefaultEmbed(f'***```{clan_name}, был удален с системы рейтинга клозов.```***'))

    @slash_command(name='close_rating', description='Посмотреть рейтинг кланов', guild_ids=[ClANS_GUILD_ID], default_permission=True)
    async def close_rating(self, inter: discord.Interaction):

        clan_rating_option = []

        for i in clan_rating_system.get_all_clan_rating_on_collection(CLANS['CLAN_TEXT_CATEGORY']):
            get_channel = self.client.get_channel(i['clan_text_id']).name
            clan_rating_option.append(discord.SelectOption(label=get_channel, description=i['clan_rating'], emoji='<:freeiconnext158790:960536938606104576>'))

        drop_down_menu = Select(options=clan_rating_option, placeholder='Список всех кланов с рейтингом')

        view = discord.ui.View(timeout=None)
        view.add_item(drop_down_menu)

        await inter.response.send_message(embed=DefaultEmbed(f'***```Select clan:```***'), view=view, ephemeral=True)

        async def menu_callback(interaction: discord.Interaction):
            text_id, clan_rating, clan_match, waiting_time = clan_rating_system.get_clan_rating_with_text_ids(drop_down_menu.values[0])
            total_time = time.gmtime(waiting_time)
            chose_channel = interaction.guild.get_channel(text_id).name
            _rating_embed = Embed(title=f'<:933511914510745640:960339525215862914> Статистика клозов клана: {chose_channel} <:933511914510745640:960339525215862914>')
            _rating_embed.add_field(name='<:933511914384920577:960339396350050406>Рейтинг клана:', value=f'***```{clan_rating}```***')
            _rating_embed.add_field(name='<:933511914707906590:960339513765429278>Всего матчей:', value=f'***```{clan_match}```***')
            _rating_embed.add_field(name='<:icons830:903836379472097332>Суммарное время игр:', value=f'***```{str(time.strftime("%H:%M:%S", total_time))}```***')
            _rating_embed.set_footer(text=f'клан крутышка!', icon_url='https://cdn.discordapp.com/emojis/960341108255260772.webp?size=80&quality=lossless')
            await interaction.response.edit_message(embed=_rating_embed, view=view)

        drop_down_menu.callback = menu_callback


def setup(client):
    client.add_cog(CloseRequest(client))
    print("Cog 'close request' connected!")
