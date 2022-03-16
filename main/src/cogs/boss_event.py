import discord
from discord import Option
from discord.commands import slash_command

from embeds.boss_event.heal_embed import HealView
from embeds.def_embed import DefaultEmbed
from clan_event.inventory_types.item_type import EnumItemTypes, Item
from config import ClANS_GUILD_ID
from embeds.boss_event.boss_embed import BossView
from cogs.base import BaseCog
from embeds.boss_event.hero_embed import HeroStatsView
from embeds.boss_event.hit_embed import HitView
from systems.boss_event_system.boss_system import boss_system
from systems.boss_event_system.hero_system import hero_system
from systems.boss_event_system.items_system import items_system


class BossBattle(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        self.client = client
        self.current_boss = None
        self.hero = None

    @slash_command(name='start', description='Start Boss Embed', guild_ids=[ClANS_GUILD_ID])
    async def start(self, interaction: discord.Interaction):
        boss = boss_system.get_random_boss()

        boss_system.boss_fight(boss)
        await interaction.response.send_message(embed=BossView(boss_system.get_current_boss()).embed)

    @slash_command(name='create_enemy', description='Start Boss Embed', guild_ids=[ClANS_GUILD_ID])
    async def create_enemy(self, ctx, name: str, health: int, attack_dmg: int, image: str):
        boss_system.create_boss(name, health, attack_dmg, image)
        await ctx.send(f'***```Boss {name} has been created```***')

    @slash_command(name='attack_enemy', description='Attack enemy', guild_ids=[ClANS_GUILD_ID])
    async def attack_enemy(self, interaction: discord.Interaction):
        hero = hero_system.get_hero_by_user(interaction.user)
        boss = boss_system.get_current_boss()

        boss.take_dmg(hero.attack_dmg)
        hero.take_dmg(boss.attack_dmg)

        await interaction.channel.send(embed=BossView(boss).embed)
        await interaction.response.send_message(embed=HitView(hero).embed, ephemeral=True)

        boss_system.change_health(boss)
        hero_system.change_health(hero)

    @slash_command(name='stats', description='Show user stats in boss event', guild_ids=[ClANS_GUILD_ID])
    async def my_stats(self, interaction: discord.Interaction):
        self.hero = hero_system.get_hero_by_user(interaction.user)

        await interaction.response.send_message(embed=HeroStatsView(self.hero).embed, ephemeral=True)

    @slash_command(name='heal_me', description='Show user stats in boss event', guild_ids=[ClANS_GUILD_ID])
    async def heal_me(self, interaction: discord.Interaction):
        hero = hero_system.get_hero_by_user(interaction.user)
        hero.full_regen()
        await interaction.response.send_message(embed=HealView(hero).embed, ephemeral=True)
        hero_system.change_health(hero)


    @slash_command(name='create_item', description='Create new item in game', guild_ids=[ClANS_GUILD_ID])
    async def create_item(self, interaction: discord.Interaction, name: str,
                       item_type: Option(str, 'chose item', choices=EnumItemTypes.list(), required=True)):

        items_system.add_new_item(item=Item(name, item_type))
        await interaction.response.send_message(
            embed=DefaultEmbed(f'***```{interaction.user.name}, вы добавили {name} типу {item_type}```***'))

    # todo  получення урону юзера в функції take_dmg |
    # todo - зробити перевірку на ха юзера, якщо вони дойшло до 0 видавати ембет і виводило час ресу
    # todo - start_battle повинно перевіряти чи є в боса хп, якщо ні то добавляти нового (перевірка attack_enemy)


def setup(client):
    client.add_cog(BossBattle(client))
    print("Cog 'boss battle' connected!")
