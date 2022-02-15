from discord.ext import commands

from cogs.base import BaseCog
from config import ClANS_GUILD_ID
from systems.money_system import money_system


class MoneyCog(BaseCog):
    def __init__(self, client):
        super().__init__(client)
        self.client = client
        self.guild = None

    @commands.Cog.listener()
    async def on_ready(self):
        if self.client:
            print('DataBase connected to money...OK!')
        else:
            print('DataBase is not connected to money...FUCK!')
            return await self.client.close()

        self.guild = self.client.get_guild(ClANS_GUILD_ID)

        for member in self.guild.members:
            money_system.add_all_clan_members_into_collection(member_id=member.id)


        # for self.guild in self.client.guilds:
        #     for member in self.guild.members:
        #         money_system.check_member(member_id=member.id)
    # @slash_command(name='timely', description=f'take {START_MONEY} money')
    # async def timely(self, ctx):
    #     author = ctx.author
    #     if not money_system.check_member(self, author_id=author.id):
    #         return money_system.member_join(self, author_id=author.id, amount=TIMELY)
    #     money_system.award(self, author_id=author.id, amount=TIMELY)
    #     return


def setup(client):
    client.add_cog(MoneyCog(client))
    print("Cog 'money' connected!")
