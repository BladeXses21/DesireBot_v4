from discord import Cog, Bot


class BaseCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.guild = None


def setup(client):
    client.add_cog(BaseCog(client))
    print("Cog 'base' connected!")
