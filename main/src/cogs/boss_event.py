from enum import Enum

import discord
from discord import Option
from discord.commands import slash_command
from embeds.def_embed import DefaultEmbed
from clan_event.life_forms.items_type import EnumItemTypes, Item
from config import ClANS_GUILD_ID
from embeds.boss_event.boss_embed import BossView
from cogs.base import BaseCog
from embeds.boss_event.hero_embed import HeroStatsView
from embeds.boss_event.hit_embed import HitView
from systems.boss_event_system.boss_system import boss_system
from systems.boss_event_system.hero_system import hero_system
from systems.boss_event_system.inventory_system import inventory_system


class BossBattle(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        self.client = client
        self.current_boss = None
        self.hero = None

    @slash_command(name='start', description='Start Boss Embed', guild_ids=[ClANS_GUILD_ID])
    async def start(self, ctx):
        boss = boss_system.get_random_boss()

        boss_system.boss_fight(boss)
        return await ctx.send(embed=BossView(boss_system.get_current_boss()).embed)

    @slash_command(name='create_enemy', description='Start Boss Embed', guild_ids=[ClANS_GUILD_ID])
    async def create_enemy(self, ctx, name: str, health: int, attack_dmg: int, image: str):
        boss_system.create_boss(name, health, attack_dmg, image)
        await ctx.send(f'***```Boss {name} has been created```***')

    @slash_command(name='attack_enemy', description='Attack enemy', guild_ids=[ClANS_GUILD_ID])
    async def attack_enemy(self, interaction: discord.Interaction):
        user = interaction.user
        self.hero = hero_system.get_hero_by_id(user.id)
        if self.hero is None:
            hero_system.create_new_hero(user)
            self.hero = hero_system.get_hero_by_id(user.id)

        boss = boss_system.get_current_boss()

        boss.take_dmg(self.hero.attack_dmg)
        self.hero.take_dmg(boss.attack_dmg)

        await interaction.response.send_message(embed=HitView(self.hero).embed, ephemeral=True)
        print(self.hero.health, '-------', boss.health)

        boss_system.change_health(boss)
        hero_system.change_health(self.hero)

        # await interaction.response.send_message(embed=BossView(boss).embed)

    @slash_command(name='stats', description='Show user stats in boss event', guild_ids=[ClANS_GUILD_ID])
    async def my_stats(self, interaction: discord.Interaction):
        user = interaction.user

        # global hero
        self.hero = hero_system.get_hero_by_id(user.id)

        # if user not exist in database yet, create him and continue command
        if self.hero is None:
            hero_system.create_new_hero(user)
            self.hero = hero_system.get_hero_by_id(user.id)

        await interaction.response.send_message(embed=HeroStatsView(self.hero).embed, ephemeral=True)

    @slash_command(name='add_item', description='add item to item collection', guild_ids=[ClANS_GUILD_ID])
    async def add_item(self, interaction: discord.Interaction, name: str, item_type: Option(str, 'chose item', choices=[EnumItemTypes.hands.value,
                                                                                                                        EnumItemTypes.spear.value,
                                                                                                                        EnumItemTypes.onion.value,
                                                                                                                        EnumItemTypes.sword.value,
                                                                                                                        EnumItemTypes.helmet.value], required=True)):
        inventory_system.add_new_item(item=Item(name, item_type))
        await interaction.response.send_message(embed=DefaultEmbed(f'***```{interaction.user.name}, вы добавили {name} типу {item_type}```***'))

    # todo - поле урону в юзерів клану, зчитувати поле урону з юзера / поле хп в юзера / получення урону юзера в функції take_dmg |
    # todo - зробити перевірку на ха юзера, якщо вони дойшло до 0 видавати ембет і виводило час ресу
    # todo - start_battle повинно перевіряти чи є в боса хп, якщо ні то добавляти нового (перевірка attack_enemy)


def setup(client):
    client.add_cog(BossBattle(client))
    print("Cog 'boss battle' connected!")
