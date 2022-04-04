from cogs.base import BaseCog
import discord
from discord.commands import permissions, slash_command, Option
from discord.ext import commands

from config import ClANS_GUILD_ID, CLAN_VOICE_CATEGORY_NAME, CLANS_ROLES, BladeXses, CLANS_EVENT_CHAT, CLAN_TEXT_CATEGORY_NAME
from embeds.clan_events_mode.close_embeds.accept_close_embed import AcceptCloseEmbed
from embeds.clan_events_mode.close_embeds.accept_close_from_events_mode import AcceptCloseFromEventMode
from embeds.clan_events_mode.close_embeds.close_request_embed import CloseRequestEmbed
from embeds.clan_events_mode.close_embeds.decline_close_embed import DeclineResponseCloseEmbed, DeclineCloseEmbed
from embeds.clan_events_mode.close_embeds.who_win import WinCloseFromEventMode
from embeds.clan_view.close_request_view_builder import close_request_view_builder
from embeds.def_embed import DefaultEmbed
from embeds.enun_clan_events_list.close_event_list import EnumCloseEventList
from systems.clan_staff.close_event_system import close_event_system


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
    @permissions.has_role(CLANS_ROLES['CLAN_CONTROL_ROLE_NAME'])
    @permissions.permission(user_id=BladeXses)
    async def close_request(self, interaction: discord.Interaction, clan: discord.TextChannel,
                            event: Option(str, 'Выберите ивент', choices=EnumCloseEventList.list(), required=True),
                            users: Option(int, 'Сколько у вас людей?', required=True),
                            comment: Option(str, 'Оставить коментарий', required=False)):
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

                async def accept_callback(ctx: discord.Interaction):
                    create_close_view.remove_item(close_request_view_builder.accept_request)
                    create_close_view.remove_item(close_request_view_builder.decline_request)

                    close_event_system.accept_close_request(message_request_id=request_in_enemy_clan.id, member_id_accept_request=ctx.user.id)

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

                    async def event_mode_accept_callback(inter: discord.Interaction):
                        clan_battle_view = close_request_view_builder.who_wining_close(clan_name_one=clan_send_name, clan_name_two=clan.name)
                        close_event_system.accept_event_mode(message_request_id=request_in_enemy_clan.id, events_mode_id=inter.user.id)
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

                            # todo - эмбеты вроде как сделаны и все работате - нужно доделать систему - сохраниения статистики - отправка сообщения в чат победившого клана -
                            #  сделать сумарное время ивента - персмотреть оформление эмбетов - рейтинг для кланов

                        async def winning_first_clan_callback(i: discord.Interaction):
                            clan_battle_view.remove_item(close_request_view_builder.first_clan_victory)
                            clan_battle_view.remove_item(close_request_view_builder.second_clan_victory)
                            await embed_in_event_chat.edit(
                                embed=WinCloseFromEventMode(clan_win=clan_send_name, clan_name_two=clan.name, event_name=event, event_mode=i.user.mention).embed,
                                view=clan_battle_view)

                        async def winning_seconds_clan_callback(i: discord.Interaction):
                            clan_battle_view.remove_item(close_request_view_builder.first_clan_victory)
                            clan_battle_view.remove_item(close_request_view_builder.second_clan_victory)
                            await embed_in_event_chat.edit(
                                embed=WinCloseFromEventMode(clan_win=clan.name, clan_name_two=clan_send_name, event_name=event, event_mode=i.user.mention).embed,
                                view=clan_battle_view)

                        close_request_view_builder.first_clan_victory.callback = winning_first_clan_callback
                        close_request_view_builder.second_clan_victory.callback = winning_seconds_clan_callback

                    async def event_mode_decline_callback(inter: discord.Interaction):
                        close_event_system.delete_close_request(message_request_id=request_in_enemy_clan.id)

                        await clan.send(embed=DefaultEmbed(f'***```{inter.user.name}, отказал в проведении клоза.```***'))

                    close_request_view_builder.event_mode_accept_request.callback = event_mode_accept_callback
                    close_request_view_builder.event_mode_decline_request.callback = event_mode_decline_callback

                async def decline_callback(ctx: discord.Interaction):
                    create_close_view.remove_item(close_request_view_builder.accept_request)
                    create_close_view.remove_item(close_request_view_builder.decline_request)
                    await response_to_a_request.edit_original_message(embed=DeclineCloseEmbed(str(ctx.user.voice.channel.name), member_decline=ctx.user.mention).embed)
                    await request_in_enemy_clan.edit(
                        embed=DeclineResponseCloseEmbed(str(interaction.user.voice.channel.name), member_decline=ctx.user.mention).embed)

                close_request_view_builder.accept_request.callback = accept_callback
                close_request_view_builder.decline_request.callback = decline_callback

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


def setup(client):
    client.add_cog(CloseRequest(client))
    print("Cog 'close request' connected!")
