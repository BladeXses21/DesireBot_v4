from embeds.def_embed import ErrorEmbed, DefaultEmbed
from base_error import on_cmd_error
from cogs.base import BaseCog
from discord.ext import commands


class ErrorHandling(BaseCog):
    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.respond(f"Нужно подождать {int(error.retry_after)}c.")

        msg = on_cmd_error(ctx, error)

        if msg:
            return await ctx.respond(embed=ErrorEmbed(msg))
        else:
            raise error  # raise other errors so they aren't ignored):


def setup(client):
    client.add_cog(ErrorHandling(client))
    print("Cog 'clans' connected!")
