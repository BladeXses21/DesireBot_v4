import time
import urllib.request

import discord
from discord import Colour, Embed, Bot
from discord.ext import commands
from discord.utils import get
from discord.commands import Option, slash_command
from discord.ui import Button

from cogs.base import BaseCog
from config import CLANS, CLANS_ROLES, ClANS_GUILD_ID
from embeds.def_embed import DefaultEmbed
from embeds.clans_embed import DeleteEmbed, ZamEmbed
from systems.clans_system import clan_system
from systems.money_system import money_system


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
        print("Cog 'clans' connected!")
        self.clans_voice_category = None
        self.clans_text_category = None
        self.leader_role = None
        self.guild = None
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

    @slash_command(name='clan_delete', description='delete your clan')
    @is_clan_leader()
    async def clan_delete(self, interaction: discord.Interaction):
        author = interaction.user
        guild = interaction.guild

        button_accept = Button(style=discord.ButtonStyle.green, label='Accept')
        button_decline = Button(style=discord.ButtonStyle.red, label='Decline')

        view = discord.ui.View()
        view.add_item(button_accept)
        view.add_item(button_decline)

        await interaction.response.send_message(embed=DefaultEmbed(f'Нужно подтверждение удаление клана.'), view=view)

        async def accept_delete(interact: discord.Interaction):

            if author != author:
                await interact.response.send_message(embed=DefaultEmbed('Hey! You can`t use that!'), ephemeral=True)
                return False
            else:
                button_accept.disabled = True
                button_decline.disabled = True
                role_id, voice_id, text_id, clan_name, img_url = clan_system.delete_clan(author.id)
                clan_role = guild.get_role(role_id)

                await author.remove_roles(self.leader_role)
                await clan_role.delete()
                await guild.get_channel(voice_id).delete()
                await guild.get_channel(text_id).delete()
                return await interact.response.edit_message(embed=DeleteEmbed(clan_name=clan_name, img_url=img_url).embed, view=view)

        async def decline_delete(interact: discord.Interaction):

            if author != author:
                await interact.response.send_message(embed=DefaultEmbed('Hey! You can`t use that!'), ephemeral=True)
                return False
            else:
                button_accept.disabled = True
                button_decline.disabled = True
                return await interact.response.edit_message(embed=DefaultEmbed(f'Удаление клана не подтверждено'), view=view)

        button_accept.callback = accept_delete
        button_decline.callback = decline_delete

    @slash_command(name='clan_create', description='Create clans', guild_ids=[ClANS_GUILD_ID])
    async def clan_create(self, interaction: discord.Interaction, color: Option(str, 'Enter clan color', required=True),
                          name: Option(str, 'Enter clan role name', required=True)):
        author = interaction.user
        guild = interaction.guild

        if clan_system.find_clan_member(member_id=author.id):
            return await interaction.response.send_message(embed=DefaultEmbed(f'***```У тебя уже есть клан.```***'), ephemeral=True)
        clan_name = ''.join(name)
        try:
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
        except TypeError | ValueError:
            return await interaction.response.send_message(embed=DefaultEmbed('***```Неправильно написан цвет.```***'), ephemeral=True)

        if len(clan_name) <= 2:
            return await interaction.response.send_message(embed=DefaultEmbed('***```Название должно содержать больше 2 символов.```***'), ephemeral=True)
        if get(author.roles, name=CLANS_ROLES['LEADER_ROLE_NAME'] or CLANS_ROLES['CONSLIGER_ROLE_NAME']):
            return await interaction.response.send_message(
                embed=DefaultEmbed(
                    f'***```Чтобы создать клан, снимите роль {CLANS_ROLES["LEADER_ROLE_NAME"]} или 'f'{CLANS_ROLES["CONSLIGER_ROLE_NAME"]}.```***'), ephemeral=True)
        # if money_system.check_member_cash(author_id=author.id) < CLANS["CLAN_CREATE_COST"]:
        #     return await ctx.respond(embed=DefaultEmbed(
        #         f"***```У вас недостаточно монет для создания клана, нужно {CLANS['CLAN_CREATE_COST']}.```***"))

        await guild.create_role(name=clan_name)
        clans_role = discord.utils.get(guild.roles, name=clan_name)
        role = guild.get_role(clans_role.id)
        await role.edit(color=Colour.from_rgb(r, g, b))
        await author.add_roles(role)

        text_channel = await guild.create_text_channel(clan_name, category=self.clans_text_category)
        overwrite = discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True, embed_links=True)
        await text_channel.set_permissions(author, overwrite=overwrite)
        await text_channel.set_permissions(clans_role, overwrite=overwrite)

        voice_channel = await guild.create_voice_channel(clan_name, category=self.clans_voice_category)
        overwrites_voice = discord.PermissionOverwrite(view_channel=True, mute_members=False, move_members=False, speak=True, connect=True)
        await voice_channel.set_permissions(author, move_members=True, mute_members=True, view_channel=True, speak=True, connect=True, priority_speaker=True)
        await voice_channel.set_permissions(clans_role, overwrite=overwrites_voice)

        clan_system.create_clan(leader_id=author.id, clan_name=clan_name, role_id=role.id, voice_id=voice_channel.id, text_id=text_channel.id, color=color,
                                create_time=int(time.time()))
        money_system.take_money_for_clan(author_id=author.id, amount=CLANS["CLAN_CREATE_COST"])
        return await interaction.edit_original_message(embed=DefaultEmbed(f'***```Клан {clan_name} был успешно создан.```***'))

    @slash_command(name='clan_invite', description='To invite a clan', guild_ids=[ClANS_GUILD_ID])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @is_clan_leader()
    async def clan_invite(self, ctx, member: Option(discord.Member, 'Enter member to invite', required=True)):
        author = ctx.author

        clan_info = clan_system.get_clan_info_by_leader_id(leader_id=author.id)
        clan_role = discord.utils.get(self.guild.roles, name=clan_info['clan_name'])
        clan_member_id = clan_system.find_clan_member(member.id)
        button1 = Button(style=discord.ButtonStyle.green, label='Accept')
        button2 = Button(style=discord.ButtonStyle.red, label='Decline')

        view = discord.ui.View()
        view.add_item(button1)
        view.add_item(button2)

        if member.bot:
            return await ctx.respond(embed=DefaultEmbed(f'***```Нельзя пригласить бота!```***'))
        if member.id is author.id:
            return await ctx.respond(embed=DefaultEmbed(f'***```Нельзя пригласить самого себя!```***'))
        if member.id == clan_member_id:
            return await ctx.respond(embed=DefaultEmbed(f'***```Пользователь уже находиться в клане!```***'))
        await ctx.respond(embed=DefaultEmbed(f'***```Вы пригласили пользователя {member} в свой клан!```***'))
        await member.send(embed=DefaultEmbed(f'***```Вы были приглашены в клан: {clan_info["clan_name"]}```***'), view=view)
        if clan_info['clan_member_number'] >= clan_info['clan_member_slot']:
            return await ctx.respond(embed=DefaultEmbed('Вы достигли лимита пользователей, докупить слоты.'))

        async def accept_callback(interaction: discord.Interaction):
            await member.add_roles(clan_role)
            clan_system.clan_invite(clan_role_id=clan_info['clan_role_id'], member_id=member.id, invite_time=int(time.time()))
            await interaction.response.send_message(embed=DefaultEmbed(f'***```Вы приняли приглашение в клан {clan_info["clan_name"]}!```***'))
            return await ctx.send(embed=DefaultEmbed(f'***```{member}, теперь участник вашего клане!```***'))

        async def decline_callback(interaction: discord.Interaction):
            await interaction.response.send_message(embed=DefaultEmbed(f'***```Вы отклонили приглашение в клан: {clan_info["clan_name"]}!```***'))
            return await ctx.send(embed=DefaultEmbed(f'***```{member}, не принял приглашение в клан!```***'))

        button1.callback = accept_callback
        button2.callback = decline_callback

    @slash_command(name='clan_kick', description='Use to kick member on your clan', guilds_ids=[ClANS_GUILD_ID])
    @is_clan_leader()
    async def clan_kick(self, ctx, member: Option(discord.Member, 'Enter member to invite', required=False)):
        author = ctx.author
        clan_member_id = clan_system.find_clan_member(member.id)
        get_clan_info_by_leader = clan_system.get_clan_info_by_leader_id(leader_id=author.id)
        get_clan_info_member = clan_system.get_clan_role_id_by_member_id(member_id=member.id)
        check_member_for_a_zam = clan_system.check_member_for_a_zam_by_member_id(member_id=member.id)

        if member.id is author.id:
            return await ctx.respond(embed=DefaultEmbed(f'***```Нельзя выгнать самого себя!```***'))
        if member.id != clan_member_id:
            return await ctx.respond(embed=DefaultEmbed(f'***```Пользователь не находиться в клане!```***'))
        if get_clan_info_by_leader['clan_role_id'] != get_clan_info_member['clan_role_id']:
            return await ctx.respond(embed=DefaultEmbed(f'***```Пользователь не в вашем клане!```***'))

        clan_name, clan_role_id = clan_system.clan_leave(member_id=member.id)

        if member.id == check_member_for_a_zam:
            clan_system.remove_zam_member_from_clan(clan_role_id=get_clan_info_member['clan_role_id'], member_id=author.id)

        return await ctx.respond(embed=DefaultEmbed(f'***```Вы кикнули {member.name} из клана {clan_name}```***'))

    @slash_command(name='clan_leave', description='Use to leave the clan', guilds_ids=[ClANS_GUILD_ID])
    @is_clan_user()
    async def clan_leave(self, ctx):
        author = ctx.author

        if clan_system.check_author_on_clan(member_id=author.id):
            return await ctx.respond(embed=DefaultEmbed('***```Не-не-не, сначало удали клан!```***'))

        if clan_system.check_member_for_a_zam_by_member_id(member_id=author.id):
            clan_name, clan_role_id = clan_system.clan_leave(member_id=author.id)
            clan_system.remove_zam_member_from_clan(clan_role_id=clan_role_id, member_id=author.id)
            return await ctx.respond(embed=DefaultEmbed(f'***```Вы успешно покинули клан {clan_name}```***'))

        clan_name, clan_role_id = clan_system.clan_leave(member_id=author.id)
        return await ctx.respond(embed=DefaultEmbed(f'***```Вы успешно покинули клан {clan_name}```***'))

    @slash_command(name='clan_profile', description='See your clan profile', guilds_ids=[ClANS_GUILD_ID])
    @is_clan_user()
    async def clan_profile(self, ctx):
        author = ctx.author
        get_clan_role = clan_system.get_clan_role_id_by_member_id(author.id)
        member_info = clan_system.clan_profile(get_clan_role['clan_role_id'])
        get_clan_info_by_role = clan_system.get_clan_info_by_role_id(get_clan_role['clan_role_id'])
        description = '**Участники кланов:**\n'
        counter = 1

        for i in member_info:
            get_member = ctx.guild.get_member(i['member_id'])

            description += f'{counter} - {get_member.mention} - {str(i["member_online"])}' + '\n'

            counter += 1

        embed = Embed(title=f'Профиль клана {get_clan_info_by_role["clan_name"]}')
        embed.add_field(name=f'Суммарный онлайн', value=f'{get_clan_info_by_role["all_online"]}')
        embed.add_field(name=f'Голосовой канал', value=f'<#{get_clan_info_by_role["voice_id"]}>')
        embed.add_field(name=f'Казна клана', value=f'{get_clan_info_by_role["clan_cash"]}', inline=False)
        embed.add_field(name=f'Дата создания', value=f'<t:{get_clan_info_by_role["create_time"]}:R>', inline=False)

        if get_clan_info_by_role['img_url']:
            embed.set_image(url=get_clan_info_by_role['img_url'])

        await ctx.respond(embed=embed)

    @slash_command(name='clan_flag', description='Set clan flag', guild_ids=[ClANS_GUILD_ID])
    @is_clan_leader()
    async def clan_flag(self, ctx, image_url):

        if image_url == 'None':
            clan_system.set_flag(leader_id=ctx.author.id, image_url=None)
            return await ctx.respond(embed=DefaultEmbed('Аватарка клана сброшена'))

        try:
            urllib.request.urlopen(image_url)
        except ValueError | TypeError:
            return await ctx.respond(embed=DefaultEmbed(f'Плохая ссылка!'))

        clan_system.set_flag(leader_id=ctx.author.id, image_url=image_url)

        return await ctx.respond(embed=DefaultEmbed('Аватарка клана обновлена'))

    @slash_command(name='clan_deposit', description='deposit money to your clan', guild_ids=[ClANS_GUILD_ID])
    @is_clan_user()
    async def clan_deposit(self, ctx, amount: Option(int, 'Enter amount to dep', required=True)):
        author = ctx.author
        get_clan_role = clan_system.get_clan_role_id_by_member_id(author.id)
        member_money = money_system.check_member_cash(author_id=author.id)

        if member_money < amount:
            return await ctx.respond(embed=DefaultEmbed(f'***```{author.name}, у вас не достаточно монет```***'))

        money_system.take_money_for_clan(author.id, int(amount))
        clan_system.clan_deposit(clan_role_id=get_clan_role['clan_role_id'], amount=int(amount))
        return await ctx.respond(embed=DefaultEmbed(f'***```{author.name}, вы закинули {amount} монет в клан!```***'))

    @slash_command(name='clan_zam', description='deposit money to your clan', guild_ids=[ClANS_GUILD_ID])
    @is_clan_leader()
    async def clan_zam(self, ctx, member: Option(discord.Member, 'specify a member to be promoted', required=True)):
        author = ctx.author
        get_clan_info = clan_system.get_clan_info_by_leader_id(leader_id=author.id)
        zam_member_id = clan_system.find_clan_zam_by_clan_role_id(clan_role_id=get_clan_info["clan_role_id"])
        get_member_info = clan_system.get_clan_role_id_by_member_id(member_id=member.id)

        if member == author:
            return await ctx.respond(embed=DefaultEmbed('***```Нет, так не пойдет!```***'))

        for i in zam_member_id["zam_member_id"]:
            if member.id == i['member_id']:
                clan_system.remove_zam_member_from_clan(clan_role_id=get_clan_info['clan_role_id'], member_id=member.id)
                return await ctx.respond(
                    embed=DefaultEmbed(f'***```{member.name}, теперь не являеться вашим заместителем```***'))

        if member.bot:
            return await ctx.respond(embed=DefaultEmbed("***```Нельзя назначить бота на заместителя```***"))

        if get_clan_info['zam_slot'] <= 0:
            return await ctx.respond(
                embed=DefaultEmbed('***```Больше не осталось свободных слотов под заместителя```***'))

        try:
            if get_member_info['clan_role_id'] != get_clan_info['clan_role_id']:
                return await ctx.respond(
                    embed=DefaultEmbed(f'***```{member.name}, не являеться участником вашего клана!```***'))
        except TypeError:
            return await ctx.respond(
                embed=DefaultEmbed(f'***```{member.name}, пользователь не состоит в вашем клане!```***'))
        clan_system.add_zam_member_to_clan(clan_role_id=get_clan_info['clan_role_id'], member_id=member.id)
        await ctx.respond(embed=ZamEmbed(author=author.name, member=member.name, clan_name=get_clan_info['clan_name'], zum_num=get_clan_info['zam_slot']).embed)

    @slash_command(name='clan_zslot', description='buy a slot for a consliger', guild_ids=[ClANS_GUILD_ID])
    @is_clan_leader()
    async def clan_zslot(self, ctx, how: Option(int, "how many slots do you want to buy", required=True)):
        author = ctx.author
        get_clan_info = clan_system.get_clan_info_by_leader_id(leader_id=author.id)

        if how > 4:
            return await ctx.respond(embed=DefaultEmbed('***```Нельзя купить больше 4 слотов заместителя.```***'))
        if get_clan_info['zam_slot'] >= 5:
            return await ctx.respond(
                embed=DefaultEmbed('***```Вы достигли максимального количества слотов для заместителя.```***'))
        if get_clan_info['clan_cash'] < how * CLANS['CLAN_CONSLIGER_COST']:
            return await ctx.respond(embed=DefaultEmbed('***```В казне не достаточно монет.```***'))

        clan_system.buy_slot_clan_zam(leader_id=author.id, how=how)
        clan_system.clan_pay(get_clan_info['clan_role_id'], amount=how * CLANS['CLAN_CONSLIGER_COST'])
        return await ctx.respond(
            embed=DefaultEmbed(f'***```{author.name}, вы приобрели {how} слотов для заместителя.```***'))

    @slash_command(name='clan_slot', description='buy a slot for a clan', guild_ids=[ClANS_GUILD_ID])
    @is_clan_leader()
    async def clan_slot(self, ctx, how: Option(int, "how many slots do you want to buy", required=True)):
        author = ctx.author
        get_clan_info = clan_system.get_clan_info_by_leader_id(leader_id=author.id)

        if get_clan_info['clan_member_slot'] >= CLANS['CLAN_MAX_MEMBER_SLOT']:
            return await ctx.respond(embed=DefaultEmbed('***```Вы достигли максимального количества слотов в клане```***'))
        if how > 25:
            return await ctx.respond(embed=DefaultEmbed('***```Нельзя купить больше 25 слотов за раз.```***'))
        if how < 5:
            return await ctx.respond(embed=DefaultEmbed('***```Покупать слоты можно не менее 5 за раз.```***'))
        if get_clan_info['clan_member_slot'] + how >= CLANS['CLAN_MAX_MEMBER_SLOT'] + 1:
            return await ctx.respond(embed=DefaultEmbed(f'***```Число слотов которое вы пытаетесь купить, превышает допустимое```***'))

        clan_system.clan_pay(get_clan_info['clan_role_id'], amount=how / 5 * CLANS["CLAN_5_SLOTS_COST"])
        clan_system.buy_clan_slot(leader_id=author.id, how=how)
        return await ctx.respond(embed=DefaultEmbed(f'***```{author.name}, вы приобрели {how} слотов для клана.```***'))


def setup(bot : Bot):
    bot.add_cog(ClansCog(bot))
