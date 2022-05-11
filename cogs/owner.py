import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from main import bot

class OwnerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[953593619288301598])
    async def ping(self, ctx):
        """Get the ping latency."""
        await ctx.defer('Pong! {0}'.format(round(bot.latency, 3)))
        
        
    @slash_command(guild_ids=[953593619288301598])
    async def servers(self, ctx):
        """Number of servers I am in."""
        await ctx.defer( f"I'm in {len(bot.guilds)} servers!")

def setup(bot):
    bot.add_cog(OwnerCommands(bot))

        

        