import discord
import os
from discord.ext import commands

from config import Token, PREFIX

client = commands.Bot(command_prefix=PREFIX, help_command=None, intents=discord.Intents.all())

for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(Token)
