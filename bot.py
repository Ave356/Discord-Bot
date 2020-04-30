import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix = '!')
TOKEN = '' # Place bot token here

#TODO add error notfication that a cog was already loaded/unloaded

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'extension "{extension}" loaded')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'extension "{extension}" unloaded')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)
