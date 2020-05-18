import os

import discord
import youtube_dl
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
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f'The bot has connect to {channel}\n')

    await ctx.send(f"Joined {channel}")
    
    
    audio_file = os.path.isfile("audio.mp3")
    try:
        if audio_file:
            os.remove("audio.mp3")
            print("Removed audio file")
    except PermissionError:
        print("Cannot delete audio file: it is being played")
        await ctx.send("Error: audio playing")
        return
    
    await ctx.send("downloading audio")
    
    voice = get(bot.voice_clients, guild=ctx.guild)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'call_home':'false',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', # 192 is the default audio quality. Change depending on your setup. https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L128-L278
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed the file: {file}")
            os.rename(file, "audio.mp3")
        
    voice.play(discord.FFmpegPCMAudio("audio.mp3"), after=lambda e: print(f"{name} has finished playing"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07 # Keep below 0.07 or lower because it becomes too loud

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("Playing\n")



@bot.command(pass_context=True, aliases=['pausing'])
async def pause(ctx):
    if bot.voice_clients and voice.is_playing():
        print('Paused')
        voice.pause()
        await ctx.send('Pausing')
        

@bot.command(pass_context=True, aliases=['resuming'])
async def resume(ctx):
    if bot.voice_clients and voice.is_paused():
        print('Resuming')
        voice.resume()
        await ctx.send('Resuming')


@bot.command(pass_context=True, aliases=['stopping'])
async def stop(ctx):
    if bot.voice_clients and voice.is_playing or voice.is_playing():
        print('Stopping')
        voice.stop()
        await ctx.send('Stopping')
        os.remove("audio.mp3")
        print("audio.mp3 removed")



bot.run(TOKEN)
