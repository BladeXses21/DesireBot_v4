import discord
import os

from config import Token

client = discord.Bot(intents=discord.Intents.all())


@client.slash_command()
async def hi(ctx):
    await ctx.respond("Hi, this is a global slash command from a cog!")


@client.event
async def on_ready():
    print("PIDOR READY")


for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(Token)
