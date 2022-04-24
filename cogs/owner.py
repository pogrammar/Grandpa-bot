import discord
from discord.ext import commands, bridge
from main import bot

class OwnerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command()
    @commands.is_owner()
    async def ping(self, ctx):
        """Get the ping latency."""
        await ctx.respond('Pong! {0}'.format(round(bot.latency, 3)))
        
        
    @bridge.bridge_command()
    @commands.is_owner()
    async def servers(self, ctx):
        """Number of servers I am in."""
        await ctx.respond( f"I'm in {len(bot.guilds)} servers!")

    #Status change commands
    @commands.group()
    @commands.is_owner()
    async def status(self, ctx):
        embed = discord.Embed(title="Status change commands", description="Below are the sub-commands to change the bot's status.", inline=False)
        embed.add_field(name="ONLINE <:Online:962781687102722068>", value="Usage: `~status online <status>`\nFunction: `Changes the bot's status to online, and status message to the one specified.`", inline=False)
        embed.add_field(name="IDLE <:Idle:962781734678716466>", value="Usage: `~status idle <status>`\nFunction: `Changes the bot's status to idle, and status message to the one specified.`", inline=False)
        embed.add_field(name="DND <:Dnd:962781703728934983>", value="Usage: `~status dnd <status>`\nFunction: `Changes the bot's status to dnd, and status message to the one specified.`", inline=False)

        await ctx.reply(embed = embed)

    @status.command()
    @commands.is_owner()
    async def online(self, ctx, *, statusmsg: str):
        await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.listening, name="~help || " + statusmsg
            )  
            )  
        await ctx.reply(f"Status set to **online** with message `{statusmsg}`")
    
    @status.command()
    @commands.is_owner()
    async def idle(self, ctx, *, statusmsg: str):
        await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Activity(
            type=discord.ActivityType.listening, name="~help || " + statusmsg
            )  
            )  
        await ctx.reply(f"Status set to **idle** with message `{statusmsg}`")
    @status.command()
    @commands.is_owner()
    async def dnd(self, ctx, *, statusmsg: str):
        await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(
            type=discord.ActivityType.listening, name="~help || " + statusmsg
            )  
            )  
        await ctx.reply(f"Status set to **dnd** with message `{statusmsg}`")

def setup(bot):
    bot.add_cog(OwnerCommands(bot))

        

        