import discord
from discord.ext import commands

TOKEN = '' # Place bot token here
client = commands.Bot(command_prefix = '!')
client = discord.Client()



client.run(TOKEN)
