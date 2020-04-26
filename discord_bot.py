import discord
from discord.ext import commands

TOKEN = '' # Be sure to place bot token here
client = commands.Bot(command_prefix = '!')
client = discord.Client()



client.run(TOKEN)