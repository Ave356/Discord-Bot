import os

import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get

bot = commands.Bot(command_prefix='!')
client = bot
class Audio_Player(commands.Cog):
    def __init__(self, bot):
        self.client = client

    
    @commands.Cog.listener()
    async def join_server(self, ctx, aliases=['Join']):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            print(f'The bot has connected to {channel}\n')
        await ctx.send(f"Joined {channel}")


    @commands.Cog.listener()
    async def leave_server(self, ctx, aliases=['leave']):
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild=ctx.guild)
    
        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"Bot has disconnected {channel}")
            await ctx.send(f"Left {channel}")
        else:
            print("Bot isn't in channel")
            await ctx.send("I am not in a channel")

    
    
    @commands.Cog.listener()
    async def pause(self, ctx, aliases=['pause']):
        if bot.voice_clients and voice.is_playing():
            print('Pausing')
            voice.pause()
            await ctx.send('Pausing')

    

    @commands.Cog.listener()
    async def resume(self, ctx, aliases=['resume']):
        if bot.voice_clients and voice.is_paused():
            print("Resuming")
            voice.resume()
            await ctx.send('Resuming')



    @commands.Cog.listener()
    async def play(self, ctx, url: str, aliases=['play']):
        audio_file = os.path.isfile("audio.mp3")
        try:
            if audio_file:
                os.remove('audio.mp3')
                print('Removed audio file')
        except PermissionError:
            print('Connot delete audio file: it is being played')
            await ctx.send('Error: audio playing')
            return
        
        await ctx.send("Downloading audio")
        voice = get (bot.voice_clients, guild=ctx.guild)

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
            if file.endwith(".mp3"):
                name = file
                print(f"Renamed the file: {file}")
                os.rename(file, "audio.mp3")

        voice.play(discord.FFmpegPCMAudio("audio.mp3"), after=lambda e: print(f"{name} has finished playing"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07 # Keep below 0.07 or lower because it becomes too loud
        
        nname = name.rsplit('-', 2)
        await ctx.send(f"Playing: {nname[0]}")
        print("Playing\n")


def setup(client):
    client.add_cog(Audio_Player(client)
