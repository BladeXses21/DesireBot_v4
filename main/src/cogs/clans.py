import time

import discord
from discord import Colour, Embed
from discord.ext import commands
from discord.utils import get
from discord.commands import Option, slash_command
from discord.ui import Button

from cogs.base import BaseCog
from config import GUILD_ID, ADMIN_ROLE, MODER_ROLE, CLANS, CLANS_ROLES, ClANS_GUILD_ID
from embeds.def_embed import DefaultEmbed
from embeds.clans_embed import DeleteEmbed
from systems.clans_system import clan_system


def is_clan_leader():
    def inner(ctx):
        if clan_system.is_clan_leader(ctx.author.id):
            return True
        raise commands.CommandError('not clan leader')

    return commands.check(inner)


def is_clan_user():
    def inner(ctx):
        if clan_system.is_clan_user(ctx.author.id):
            return True
        raise commands.CommandError('not clan user')

    return commands.check(inner)


class ClansCog(BaseCog):

    def __init__(self, client):
        super().__init__(client)
        self.client = client
        self.clans_voice_category = None
        self.clans_text_category = None
        self.leader_role = None
        self.guild = None
        self.create_time = None
        self.everyone_role = None

    @commands.Cog.listener()
    async def on_ready(self):
        if self.client:
            print('DataBase connected to clans...OK!')
        else:
            print('DataBase is not connected to clans...FUCK!')
            return await self.client.close()

        self.guild = self.client.get_guild(ClANS_GUILD_ID)

        self.clans_voice_category = self.client.get_channel(CLANS['CLAN_VOICE_CATEGORY'])
        self.clans_text_category = self.client.get_channel(CLANS['CLAN_TEXT_CATEGORY'])

        if not self.clans_text_category or not self.clans_voice_category:
            print('Cannot find CLANS_CATEGORY in guild')
            await self.client.close()

        self.leader_role = discord.utils.get(self.guild.roles, name=CLANS_ROLES['LEADER_ROLE_NAME'])
        self.everyone_role = discord.utils.get(self.guild.roles, name="@everyone")
        self.create_time = int(time.time())

    @slash_command(name='clans', guild_ids=[ClANS_GUILD_ID])
    async def clans(self, ctx):
        await ctx.respond("Hi, this is a global slash command from a cog!")

    @slash_command(name='clan_delete', description='delete your clan')
    @is_clan_leader()
    async def clan_delete(self, ctx):
        author = ctx.author
        guild = ctx.guild
        clan_info = clan_system.get_clan_info(author.id)

        role_id, voice_id, text_id = clan_system.delete_clan(author.id)
        clan_role = guild.get_role(role_id)

        await author.remove_roles(self.leader_role)
        await clan_role.delete()
        await guild.get_channel(voice_id).delete()
        await guild.get_channel(text_id).delete()

        return await ctx.respond(embed=DeleteEmbed(author=author, clan_name=clan_info['clan_name']))

    @slash_command(name='clan_create', description='Create clans', guild_ids=[ClANS_GUILD_ID])
    async def clan_create(self, ctx, color: Option(str, 'Enter clan color', required=True),
                          name: Option(str, 'Enter clan role name', required=True)):
        author = ctx.author
        guild = ctx.guild
        clan_name = ''.join(name)
        try:
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
        except:
            return await ctx.respond(embed=DefaultEmbed('***```Неправильно написан цвет.```***'))

        if len(clan_name) <= 2:
            return await ctx.respond(embed=DefaultEmbed('***```Название должно содержать больше 2 символов.```***'))
        if get(author.roles, name=CLANS_ROLES['LEADER_ROLE_NAME'] or CLANS_ROLES['CONSLIGER_ROLE_NAME']):
            return await ctx.respond(
                embed=DefaultEmbed(f'***```Чтобы создать клан, снимите роль {CLANS_ROLES["LEADER_ROLE_NAME"]} или '
                                   f'{CLANS_ROLES["CONSLIGER_ROLE_NAME"]}.```***'))
        # Проверка на необходимое количество конфет
        # return await ctx.respond(embed=DefaultEmbed(f"У вас недостаточно монет для создания клана, нужно {CLANS['CLAN_CREATE_COST']}.```***"))

        await ctx.guild.create_role(name=clan_name)
        clans_role = discord.utils.get(guild.roles, name=clan_name)
        role = guild.get_role(clans_role.id)
        await role.edit(color=Colour.from_rgb(r, g, b))
        msg = await ctx.send(embed=DefaultEmbed(f'***```Роль клана {clan_name} была успешно создана.```***'))

        text_channel = await guild.create_text_channel(clan_name, category=self.clans_text_category)
        overwrite = discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True,
                                                embed_links=True)
        await text_channel.set_permissions(author, overwrite=overwrite)
        await text_channel.set_permissions(clans_role, overwrite=overwrite)
        await msg.edit(embed=DefaultEmbed(f'***```Текстовый канал {clan_name} был создан успешно.```***'))

        voice_channel = await guild.create_voice_channel(clan_name, category=self.clans_voice_category)
        overwrites_voice = discord.PermissionOverwrite(view_channel=True, mute_members=False, move_members=False,
                                                       speak=True, connect=True)
        await voice_channel.set_permissions(author, move_members=True, mute_members=True, view_channel=True, speak=True,
                                            connect=True, priority_speaker=True)
        await voice_channel.set_permissions(clans_role, overwrite=overwrites_voice)
        await msg.edit(embed=DefaultEmbed(f'***```Войс клана {clan_name} был успешно создан.```***'))
        print(clan_name, author, role.name, text_channel.id, voice_channel.id, self.create_time)

        clan_system.create_clan(leader_id=author.id, clan_name=clan_name, role_id=role.id, voice_id=voice_channel.id,
                                text_id=text_channel.id, create_time=self.create_time)
        await msg.edit(embed=DefaultEmbed(f'***```Клан {clan_name} был успешно создан.```***'))

    @slash_command(name='clan_invite', description='To invite a clan', guild_ids=[ClANS_GUILD_ID])
    @is_clan_leader()
    async def clan_invite(self, ctx, member: Option(discord.Member, 'Enter member to invite', required=True)):
        author = ctx.author

        clan_info = clan_system.get_clan_info(leader_id=author.id)
        clan_role = discord.utils.get(self.guild.roles, name=clan_info['clan_name'])
        clan_member_id = clan_system.find_clan_member(member.id)
        button1 = Button(style=discord.ButtonStyle.green, label='Accept')
        button2 = Button(style=discord.ButtonStyle.red, label='Decline')

        view = discord.ui.View()
        view.add_item(button1)
        view.add_item(button2)

        if member.id is author.id:
            return await ctx.respond(embed=DefaultEmbed(f'***```Нельзя пригласить самого себя!```***'))
        if member.id == clan_member_id:
            return await ctx.respond(embed=DefaultEmbed(f'***```Пользователь уже находиться в клане!```***'))
        await ctx.respond(embed=DefaultEmbed(f'***```Вы пригласили пользователя {member} в свой клан!```***'))
        await member.send(embed=DefaultEmbed(f'***```Вы были приглашены в клан: {clan_info["clan_name"]}```***'),
                          view=view)

        async def AcceptCallback(interaction: discord.Interaction):
            await member.add_roles(clan_role)
            clan_system.clan_invite(clan_role_id=clan_info['clan_role_id'], member_id=member.id,
                                    invite_time=self.create_time)
            await interaction.response.send_message(
                embed=DefaultEmbed(f'***```Вы приняли приглашение в клан {clan_info["clan_name"]}!```***'))
            return await ctx.send(embed=DefaultEmbed(f'***```{member}, теперь участник вашего клане!```***'))

        async def DeclineCallback(interaction: discord.Interaction):
            await interaction.response.send_message(
                embed=DefaultEmbed(f'***```Вы отклонили приглашение в клан: {clan_info["clan_name"]}!```***'))
            return await ctx.send(embed=DefaultEmbed(f'***```{member}, не принял приглашение в клан!```***'))

        button1.callback = AcceptCallback
        button2.callback = DeclineCallback

    @slash_command(name='clan_profile', description='See your clan profile', guilds_ids=[ClANS_GUILD_ID])
    async def clan_profile(self, ctx):
        author = ctx.author
        get_clan_role = clan_system.get_clan_role_by_member_id(author.id)
        member_info = clan_system.clan_profile(get_clan_role['clan_role_id'])
        get_clan_name = clan_system.get_clan_info_by_role_id(get_clan_role['clan_role_id'])
        description = '**Участники кланов:**\n'
        counter = 1

        for i in member_info:
            get_member = ctx.guild.get_member(i['member_id'])

            description += f'{counter} - {get_member.mention} - {str(i["member_online"])}' + '\n'

            counter += 1

        embed = Embed(title=f'Профиль клана {get_clan_name["clan_name"]}', description=description)
        embed.add_field(name=f'Всего времени', value=f'{get_clan_name["all_online"]}')
        embed.add_field(name=f'Голосовой канал', value=f'<#{get_clan_name["voice_id"]}>')
        embed.add_field(name=f'Дата создания', value=f'<t:{get_clan_name["create_time"]}>', inline=False)

        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(ClansCog(client))
    print("Cog 'clans' connected!")
