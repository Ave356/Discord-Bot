import os

import discord
from discord.ext import commands
from discord.utils import get


bot = commands.Bot(command_prefix = '!')
TOKEN = open("place-token-here.txt", "r").readline() 


#TODO add error notfication that a cog was already loaded/unloaded


@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'extension "{extension}" loaded')


@bot.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'extension "{extension}" unloaded')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')



bot.run(TOKEN)
