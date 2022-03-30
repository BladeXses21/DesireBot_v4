import discord
from discord import slash_command, Interaction, Option, Bot
from discord.ext import commands

from clan_event.inventory_types.item_type import Item, EnumItemTypes
from cogs.base import BaseCog
from config import PREFIX, ClANS_GUILD_ID
from embeds.boss_event.battle_embed import BattleView
from embeds.boss_event.boss_drop_embed import BossDropView
from embeds.boss_event.heal_embed import HealView
from embeds.boss_event.inventory_embed import HeroInventoryView
from embeds.def_embed import DefaultEmbed
from systems.boss_event_system.battle_system import battle_system
from systems.boss_event_system.boss_system import boss_system
from systems.boss_event_system.hero_system import hero_system
from systems.boss_event_system.items_system import items_system


class BossGameAdmin(BaseCog):
    def __init__(self, bot: Bot):
        super().__init__(bot)
        print("Cog 'boss-game admin commands' connected!")

    @commands.group(name='admin', description="Список команд для адмінів")
    async def admin(self, ctx):
        if not ctx.invoked_subcommand:
            return await ctx.send(embed=DefaultEmbed(f'1. {PREFIX + "boss"} start - Start Boss Game\n'
                                                     f'2. {PREFIX + "boss"} create_enemy - Create enemy\n'
                                                     f'3. {PREFIX + "boss"} create_item - Create item\n'
                                                     f'4. {PREFIX + "boss"} add_boss_drop_item - Add item to boss\n'
                                                     f'5. {PREFIX + "boss"} heal_me - Resurrect and heal'))

    @slash_command(name='start', description='Start Boss Embed', guild_ids=[ClANS_GUILD_ID])
    async def start(self, interaction: Interaction):
        boss = boss_system.get_random_boss()
        battle_system.start_new_battle(boss)
        #     todo event start embed
        await interaction.response.send_message(
            embed=DefaultEmbed(description=f'***```Boss {boss.name} was born in hell to destroy the world!```***'))

    @slash_command(name='create_enemy', description='Start Boss Embed', guild_ids=[ClANS_GUILD_ID])
    async def create_enemy(self, interaction: Interaction, name: str, health: int, attack_dmg: int, image: str):
        boss_system.create_boss(name, health, attack_dmg, image)
        await interaction.response.send_message(f'***```Boss {name} has been created```***')

    @slash_command(name='create_item', description='Create new item in game', guild_ids=[ClANS_GUILD_ID])
    async def create_item(self, interaction: Interaction, name: str,
                          item_type: Option(str, 'choose item type', choices=EnumItemTypes.list(), required=True)):
        items_system.create_new_item(item=Item(name=name, type=item_type))
        await interaction.response.send_message(
            embed=DefaultEmbed(f'***```{interaction.user.name}, вы добавили {name} типу {item_type}```***'))

    @slash_command(name='heal_me', description='Show user stats in boss event', guild_ids=[ClANS_GUILD_ID])
    async def heal_me(self, interaction: Interaction):
        hero = hero_system.get_hero_by_user(interaction.user)
        hero.full_regen()
        await interaction.response.send_message(embed=HealView(hero).embed, ephemeral=True)
        hero_system.health_change(hero)

    @slash_command(name='take_item', description='Add item to current player inventory', guild_ids=[ClANS_GUILD_ID])
    async def take_item(self, interaction: discord.Interaction, item_name: str):
        hero = hero_system.get_hero_by_user(interaction.user)

        item = items_system.find_by_name(item_name)
        if item is None:
            await interaction.response.send_message(embed=HeroInventoryView(hero).embed)
            return

        hero.inventory.add_item(item)

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


def setup(bot):
    bot.add_cog(BossGameAdmin(bot))
