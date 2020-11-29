import discord 
from discord.ext import commands
import random


class EightBall(commands.Cog):
    def __init__(self, client):
        self.client = client

        @client.command(pass_context=True)
        async def eightball(ctx):
            magic_ball = ['As I see it, yes.',
            'Ask Again later.',
            'Better not tell you now',
            'Cannot predict now.',
            'Concentrate and ask again.',
            "Don't count on it.",
            'It is certain.',
            'It is decidedly so.',
            'Most likely',
            'My reply is no',
            'My sources say no.',
            'Outlook not so good',
            'Outlook not so good',
            'Outlook good.',
            'Reply hazy, try again.',
            'Very doubtful',
            'Signs point to yes',
            'Without a doubt.',
            'Yes.',
            'Yes - definitely.',
            'You may rely on it']
            
            await ctx.send(random.choice(magic_ball))


def setup(client):
    client.add_cog(EightBall(client))