from cogs.base import BaseCog
import discord
from discord.commands import permissions, slash_command, Option
from discord.ext import commands
from discord.ui import Button

from config import ClANS_GUILD_ID, CLAN_VOICE_CATEGORY_NAME, CLANS_ROLES, BladeXses, Less, CLANS_EVENT_CHAT, CLAN_TEXT_CATEGORY_NAME
from embeds.clan_events_mode.accept_close_embed import AcceptCloseEmbed
from embeds.clan_events_mode.close_request_embed import CloseRequestEmbed
from embeds.clan_events_mode.decline_close_embed import DeclineResponseCloseEmbed, DeclineCloseEmbed
from embeds.def_embed import DefaultEmbed
from enun_clan_events_list.close_event_list import EnumCloseEventList


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
        button_accept_request = Button(style=ButtonStyle.secondary, label='Принять вызов', emoji='✔')
        button_decline_request = Button(style=ButtonStyle.secondary, label='Отклонить вызов', emoji='❌')

        view = discord.ui.View(timeout=None)
        view.add_item(button_accept_request)
        view.add_item(button_decline_request)

        if users <= 4:
            return await interaction.response.send_message(embed=DefaultEmbed('***```Нужно минимум 5 человек.```***'))

        if clan.name in clan_text_channel_list(interaction):
            if interaction.user.id in clan_voice_channel_list(interaction):
                response_to_a_request = await interaction.response.send_message(
                    embed=DefaultEmbed(f'***```{interaction.user.name}, вы успешно отправили вызов клану {clan}```***'))
                request_in_enemy_clan = await clan.send(
                    embed=CloseRequestEmbed(clan_name=clan.name, event_name=event, interaction=interaction, members_on_voice=users, comment=comment).embed, view=view)

                async def accept_callback(ctx: discord.Interaction):
                    view.remove_item(button_accept_request)
                    view.remove_item(button_decline_request)
                    await response_to_a_request.edit_original_message(
                        embed=AcceptCloseEmbed(clan_name_requesting=str(interaction.user.voice.channel.name), clan_name_accepted=ctx.user.voice.channel.name,
                                               event_name=event, member_request=interaction.user.mention, member_accepted=ctx.user.mention, comment=comment).embed)
                    await request_in_enemy_clan.edit(
                        embed=AcceptCloseEmbed(clan_name_requesting=str(interaction.user.voice.channel.name), clan_name_accepted=ctx.user.voice.channel.name,
                                               event_name=event, member_request=interaction.user.mention, member_accepted=ctx.user.mention, comment=comment).embed)
                    await self.clan_event_chat.send(
                        embed=AcceptCloseEmbed(clan_name_requesting=str(interaction.user.voice.channel.name), clan_name_accepted=ctx.user.voice.channel.name,
                                               event_name=event, member_request=interaction.user.mention, member_accepted=ctx.user.mention, comment=comment).embed)

                async def decline_callback(ctx: discord.Interaction):
                    view.remove_item(button_accept_request)
                    view.remove_item(button_decline_request)
                    await response_to_a_request.edit_original_message(embed=DeclineCloseEmbed(str(ctx.user.voice.channel.name), member_decline=ctx.user.mention).embed)
                    await request_in_enemy_clan.edit(
                        embed=DeclineResponseCloseEmbed(str(interaction.user.voice.channel.name), member_decline=ctx.user.mention).embed)

                button_accept_request.callback = accept_callback
                button_decline_request.callback = decline_callback

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
                    clans_channels_collection += f'**{counter}** - ' + f'**`{channel.name}`**' + '\n'
        return await ctx.send(embed=DefaultEmbed(clans_channels_collection), delete_after=20)


def setup(client):
    client.add_cog(CloseRequest(client))
    print("Cog 'close request' connected!")
