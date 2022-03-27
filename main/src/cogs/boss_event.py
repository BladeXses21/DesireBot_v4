import discord
from discord import Option
from discord.commands import slash_command
from discord.ui import Button
from discord.ext import commands
from embeds.boss_event.battle_embed import BattleView
from embeds.boss_event.boss_drop_embed import BossDropView
from embeds.boss_event.heal_embed import HealView
from embeds.boss_event.inventory_embed import HeroInventoryView
from embeds.def_embed import DefaultEmbed
from clan_event.inventory_types.item_type import EnumItemTypes, Item
from config import ClANS_GUILD_ID, PREFIX
from embeds.boss_event.boss_embed import BossView
from cogs.base import BaseCog
from embeds.boss_event.hero_embed import HeroStatsView
from embeds.boss_event.hit_embed import HitView
from systems.boss_event_system.battle_system import battle_system
from systems.boss_event_system.boss_system import boss_system
from systems.boss_event_system.hero_system import hero_system
from systems.boss_event_system.items_system import items_system


class BossBattle(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        self.client = client

    @commands.group(name='admin', description="Список команд для адмінів")
    async def admin(self, ctx):
        if not ctx.invoked_subcommand:
            return await ctx.send(embed=DefaultEmbed(f'**1. {PREFIX + "boss"} start - Start Boss Embed\n'
                                                     f'2. {PREFIX + "boss"} create_enemy - Create enemy\n'
                                                     f'3. {PREFIX + "boss"} create_item - create item\n'
                                                     f'4. {PREFIX + "boss"} add_boss_drop_item - add item to boss\n'
                                                     f'5. {PREFIX + "boss"} heal_me - how user stats in boss event'))

    @slash_command(name='start', description='Start Boss Embed', guild_ids=[ClANS_GUILD_ID])
    async def start(self, interaction: discord.Interaction):
        boss = boss_system.get_random_boss()

        battle = battle_system.start_new_battle(boss)
        # Todo create embed for battle info/ instead of boss view
        await interaction.response.send_message(embed=BattleView(battle, interaction.user).embed)

    @slash_command(name='boss', description='Start Boss Embed', guild_ids=[ClANS_GUILD_ID])
    async def boss(self, interaction: discord.Interaction):
        button_attack = Button(style=discord.ButtonStyle.green, label='Attack', emoji="🗡")
        button_stats = Button(style=discord.ButtonStyle.red, label='Stats', emoji='💎')

        view = discord.ui.View()
        view.add_item(button_attack)
        view.add_item(button_stats)
        battle = battle_system.get_current_battle()
        boss_embed = await interaction.response.send_message(embed=BattleView(battle, interaction.user).embed, view=view, ephemeral=True)

        async def attack_callback(interact: discord.Interaction):
            if interact.user != interaction.user:
                return await interact.response.send_message(embed=DefaultEmbed('***```Команду визвав не ти.```***'), ephemeral=True)
            hero = hero_system.get_hero_by_user(interact.user)

            battle.fight_with(hero)

            battle_system.record_dealt_dmg(battle)
            hero_system.health_change(hero)

            return await interact.response.send_message(embed=HitView(hero).embed, ephemeral=True)

        async def stats_callback(inter: discord.Interaction):
            if inter.user.id != interaction.user.id:
                return await inter.response.send_message(embed=DefaultEmbed('***```Команду визвав не ти.```***'), ephemeral=True)

            hero = hero_system.get_hero_by_user(interaction.user)
            return await inter.response.send_message(embed=HeroStatsView(hero).embed, ephemeral=True)

        button_attack.callback = attack_callback
        button_stats.callback = stats_callback

    @slash_command(name='create_enemy', description='Start Boss Embed', guild_ids=[ClANS_GUILD_ID])
    async def create_enemy(self, interaction: discord.Interaction, name: str, health: int, attack_dmg: int, image: str):
        boss_system.create_boss(name, health, attack_dmg, image)
        await interaction.response.send_message(f'***```Boss {name} has been created```***')

    @slash_command(name='attack_enemy', description='Attack enemy', guild_ids=[ClANS_GUILD_ID])
    async def attack_enemy(self, interaction: discord.Interaction):
        hero = hero_system.get_hero_by_user(interaction.user)
        if hero.is_dead():
            await interaction.response.send_message(embed=DefaultEmbed(f'***```You cant attack being dead !!!```***'))
            return

        battle = battle_system.get_current_battle()

        if battle.is_over():
            boss = boss_system.get_random_boss()
            battle = battle_system.start_new_battle(boss)

            # todo embed for boss spawn
            await interaction.channel.send(
                embed=DefaultEmbed(f'***```Boss {boss.name} was born in hell to destroy the world!```***'))
            await interaction.channel.send(embed=BattleView(battle, interaction.user).embed)

        battle.fight_with(hero)

        battle_system.update_current_battle(battle)
        hero_system.health_change(hero)
        await interaction.response.send_message(embed=HitView(hero).embed, ephemeral=True)

        if battle.is_over():
            # todo embed for epic boss dead
            await interaction.channel.send(embed=DefaultEmbed(f'***```Boss is dead!!!```***'))

            return

        await interaction.channel.send(embed=BossView(battle.enemy).embed)

    @slash_command(name='stats', description='Show user stats in boss event', guild_ids=[ClANS_GUILD_ID])
    async def my_stats(self, interaction: discord.Interaction):
        hero = hero_system.get_hero_by_user(interaction.user)
        await interaction.response.send_message(embed=HeroStatsView(hero).embed, ephemeral=True)

    @slash_command(name='heal_me', description='Show user stats in boss event', guild_ids=[ClANS_GUILD_ID])
    async def heal_me(self, interaction: discord.Interaction):
        hero = hero_system.get_hero_by_user(interaction.user)
        hero.full_regen()
        await interaction.response.send_message(embed=HealView(hero).embed, ephemeral=True)
        hero_system.health_change(hero)

    @slash_command(name='create_item', description='Create new item in game', guild_ids=[ClANS_GUILD_ID])
    async def create_item(self, interaction: discord.Interaction, name: str,
                          item_type: Option(str, 'choose item type', choices=EnumItemTypes.list(), required=True)):
        items_system.create_new_item(item=Item(name=name, type=item_type))
        await interaction.response.send_message(
            embed=DefaultEmbed(f'***```{interaction.user.name}, вы добавили {name} типу {item_type}```***'))

    @slash_command(name='inventory', description='Show your inventory', guild_ids=[ClANS_GUILD_ID])
    async def inventory(self, interaction: discord.Interaction):
        hero = hero_system.get_hero_by_user(interaction.user)
        await interaction.response.send_message(embed=HeroInventoryView(hero).embed)

    @slash_command(name='take_item', description='Show your inventory', guild_ids=[ClANS_GUILD_ID])
    async def take_item(self, interaction: discord.Interaction, item_name: str):
        hero = hero_system.get_hero_by_user(interaction.user)

        item = items_system.find_by_name(item_name)
        if item is None:
            await interaction.response.send_message(embed=HeroInventoryView(hero).embed)
            return

        hero.inventory.add_item(item)

        hero_system.modify_inventory(hero)
        await interaction.response.send_message(embed=HeroInventoryView(hero).embed)

    @slash_command(name='equip_item', description='equip item from your inventory', guild_ids=[ClANS_GUILD_ID])
    async def equip_item(self, interaction: discord.Interaction, item_index: int):
        hero = hero_system.get_hero_by_user(interaction.user)
        inventory = hero.inventory
        inventory.equip(inventory.item_by_index(item_index))

        hero_system.modify_inventory(hero)
        await interaction.response.send_message(embed=HeroInventoryView(hero).embed)

    @slash_command(name='remove_item', description='remove item from your inventory', guild_ids=[ClANS_GUILD_ID])
    async def remove_item(self, interaction: discord.Interaction, item_index: int):
        hero = hero_system.get_hero_by_user(interaction.user)
        inventory = hero.inventory
        inventory.remove_item(item_index)

        hero_system.modify_inventory(hero)
        await interaction.response.send_message(embed=HeroInventoryView(hero).embed)

    @slash_command(name='add_boss_drop', description='add item drop for boss', guild_ids=[ClANS_GUILD_ID])
    async def add_boss_drop(self, interaction: discord.Interaction, boss_name: str, item_name: str):
        boss = boss_system.get_by_name(boss_name)
        inventory = boss.inventory
        item = items_system.find_by_name(item_name)
        if item is None:
            await interaction.response.send_message(embed=DefaultEmbed("```Item doesnt exist```"))
            return
        inventory.add_item(item)

        boss_system.modify_inventory(boss)
        await interaction.response.send_message(embed=BossDropView(boss).embed)

    @slash_command(name='remove_boss_drop', description='remove item drop from boss', guild_ids=[ClANS_GUILD_ID])
    async def remove_boss_drop(self, interaction: discord.Interaction, boss_name: str, item_index: int):
        boss = boss_system.get_by_name(boss_name)
        boss.inventory.remove_item(item_index)

        boss_system.modify_inventory(boss)
        await interaction.response.send_message(embed=BossDropView(boss).embed)

    @slash_command(name='see_boss_inventory', description='show boss inventory', guild_ids=[ClANS_GUILD_ID])
    async def see_boss_inventory(self, interaction: discord.Interaction, boss_name: str):
        boss = boss_system.get_by_name(boss_name)
        await interaction.response.send_message(embed=BossDropView(boss).embed)


def setup(client):
    client.add_cog(BossBattle(client))
    print("Cog 'boss battle_types' connected!")
