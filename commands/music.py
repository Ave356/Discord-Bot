import os

import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get

TOKEN = '' # Place bot token here

bot = commands.Bot(command_prefix='!')

#TODO Make music.py into a loadable cog
# potentially turn this into a loadable cog

@bot.command(pass_context=True, aliases=['join'])
async def join_server(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f'The bot has connect to {channel}\n')

    await ctx.send(f"Joined {channel}")



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
        await ctx.send("I am not in a channel")




@bot.command(pass_context=True, aliases=['player'])
async def play(ctx,url: str):
    song_file= os.path.isfile("song.mp3")
    try:
        if song_file:
            os.remove("song.mp3")
            print("Removed song file")
    except PermissionError:
        print("Cannot delete song file: it is being played")
        await ctx.send("Error: Song playing")
        return
    
    await ctx.send("Downloading song")
    
    voice = get(bot.voice_clients, guild=ctx.guild)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', # default audio quality. Change depending on your setup. https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L128-L278
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed the file: {file}")
            os.rename(file, "song.mp3")
        
    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} has finished playing"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07 # Keep below 0.07 or lower because it becomes too loud

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("Playing\n")



bot.run(TOKEN)
