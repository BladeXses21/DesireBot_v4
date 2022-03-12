from discord.commands import slash_command
from config import ClANS_GUILD_ID
from embeds.boss_event_embed import BossView
from cogs.base import BaseCog
from systems.boss_event_system import event_system
from clan_event.boss_type import Enemy
from clan_event.user_type import User
import discord


class BossBattle(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        self.client = client
        self.current_boss = None

    @slash_command(name='start', description='Start Boss Embed', guild_ids=[ClANS_GUILD_ID])
    async def start(self, ctx):
        boss = event_system.get_random_boss()

        event_system.boss_fight(boss)
        return await ctx.send(embed=BossView(event_system.get_current_boss()).embed)

    @slash_command(name='create_enemy', description='Start Boss Embed', guild_ids=[ClANS_GUILD_ID])
    async def create_enemy(self, ctx, name: str, health: int, atack_dmg: int, image: str):
        event_system.create_boss(name=name, health=health, atack_dmg=atack_dmg, image=image)
        await ctx.send(f'***```Boss {name} has been created```***')

    @slash_command(name='atack', description='Atack enemy', guild_ids=[ClANS_GUILD_ID])
    async def atack(self, interaction: discord.interactions):
        user = event_system.get_user_who_atack(member_id=interaction.user.id)
        boss = event_system.get_current_boss()
        print(user, '-------', boss)
        boss.take_dmg(1)
        user.take_dmg(1)
        event_system.change_health_current_boss(boss)
        await interaction.response.send_message(embed=BossView(boss).embed)

    # todo - поле урону в юзерів клану, зчитувати поле урону з юзера / поле хп в юзера / получення урону юзера в функції take_dmg | створити клас User✔ |
    # todo - зробити перевірку на ха юзера, якщо вони дойшло до 0 видавати ембет і виводило час ресу
    # todo - start_battle повинно перевіряти чи є в боса хп, якщо ні то добавляти нового (перевірка atack_enemy)


def setup(client):
    client.add_cog(BossBattle(client))
    print("Cog 'boss battle' connected!")
