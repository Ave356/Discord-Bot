import os

import discord
from yt_dlp import YoutubeDL
from discord.ext import commands
from discord.utils import get


class AudioPlayer(commands.Cog):
    def __init__(self, client):
        self.client = client


        @client.command(pass_context=True)
        async def join(ctx):
            global voice 
            channel = ctx.message.author.voice.channel
            voice = get(client.voice_clients, guild=ctx.guild)

            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
                print(f"Bot has connected to {channel}\n")

        
        @client.command(pass_context=True)
        async def leave(ctx):
            channel = ctx.message.author.voice.channel
            voice = get(client.voice_clients, guild=ctx.guild)

            if voice and voice.is_connected():
                await voice.disconnect()
                print(f"Bot has disconnected from {channel}")
            else:
                print("Bot isn't in a channel")
                await ctx.send("I am not in a channel")


        @client.command(pass_context=True)
        async def play(ctx,url: str):
            global voice 
            channel = ctx.message.author.voice.channel
            voice = get(client.voice_clients, guild=ctx.guild)

            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
                print(f"the bot has connected to {channel}\n")
                        
            
            audio_file = os.path.isfile("audio.flac")
            try:
                if audio_file:
                    os.remove("audio.flac")
                    print("Removed audio file")
            except PermissionError:
                print("Cannot delete audio file: it is being played")
                await ctx.send("Error: audio playing")
                return
            
            
            voice = get(client.voice_clients, guild=ctx.guild)
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'external_downloader': 'aria2c',
                'call_home':'false',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'flac',
                    'preferredquality': '142', # 192 is the default audio quality. Change depending on your setup. https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L128-L278
                }],
            }

            with YoutubeDL(ydl_opts) as ydl:
                print("Downloading audio\n")
                ydl.download([url])

            for file in os.listdir("./"):
                if file.endswith(".flac"):
                    name = file
                    print(f"Renamed the file: {file}")
                    os.rename(file, "audio.flac")
                
            voice.play(discord.FFmpegPCMAudio("audio.flac"), after=lambda e: print(f"{name} has finished playing"))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.3 # Keep at 0.3 or lower else it becomes too loud

            nname = name.rsplit("-", 2)
            await ctx.send(f"Playing: {nname[0]}")
            print("Playing\n")


        @client.command(pass_context=True)
        async def pause(ctx):
            if client.voice_clients and voice.is_playing():
                print("Pausing")
                voice.pause()
                await ctx.send('Pausing')
            else:
                print('Not currently playing anything')


        @client.command(pass_context=True)
        async def resume(ctx):
            if client.voice_clients and voice.is_paused():
                print("Resuming")
                voice.resume()
                await ctx.send('Resuming')


        @client.command(pass_context=True)
        async def stop(ctx):
            if client.voice_clients and voice.is_playing():
                print("Stopping")
                voice.stop()
                await ctx.send('Stopping')
            if os.path.exists("audio.flac"):
                os.remove("audio.flac")
                print("removing audio.flac")

def setup(client):
    client.add_cog(AudioPlayer(client))
