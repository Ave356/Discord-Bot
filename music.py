import discord
from discord.ext import commands
from discord.utils import get
import os
import youtube_dl



#TODO add music playing functionality
# potentially this into a loadable cog


TOKEN = '' # Place bot token here
bot = commands.Bot(command_prefix='!')



@bot.command(pass_context=True, aliases=['join'])
async def joined(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f'The bot has connect to {channel}\n')

    await ctx.send(f"Joined {channel}")


    #await voice.disconnect()

    #if voice and voice.is_connected():
        #await voice.move_to(channel)
    #else:
       # voice = await channel.connect()

@bot.command(pass_context=True, aliases=['leave'])
async def leave_server(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    
    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"Bot has disconnected {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot isn't in channel")
        await ctx.send("Bot not in a channel")

        
bot.run(TOKEN)
