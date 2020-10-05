import discord
import random
from discord.ext import commands

# user needs admin permission in order to run this cog

class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client

        @client.command(pass_context=True)
        @commands.has_permissions(manage_messages=True)
        async def clear(ctx, amount=5): # change amount depending on how many messages you want to be deleted
            await ctx.channel.purge(limit=amount)

        @client.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.MissingPermissions):
                print("User does not have permission")
                await ctx.send("You do not have permission to run the command")

def setup(client):
    client.add_cog(Clear(client))
