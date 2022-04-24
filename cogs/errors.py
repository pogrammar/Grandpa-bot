import discord
from discord.ext import commands
import math

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # if command has local error handler, return
        if hasattr(ctx.command, 'on_error'):
            return

        # get the original exception
        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            await ctx.reply("Command not found.")
            return

        if isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'I need the **{}** permission(s) to run this command.'.format(fmt)
            await ctx.reply(_message)
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.reply('This command has been disabled.')
            return

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply("This command is on cooldown, please retry in {}s.".format(math.ceil(error.retry_after)))
            return

        if isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
            await ctx.reply(_message)
            return

        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.reply('This command cannot be used in direct messages.')
            except discord.Forbidden:
                pass
            return
        if isinstance(error, discord.errors.NotFound):
            await ctx.author.reply("Internet error.")
        if isinstance(error, discord.errors.Forbidden):
                pass
    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
                # if command has local error handler, return
        if hasattr(ctx.command, 'on_error'):
            return

        # get the original exception
        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            await ctx.respond("Command not found.")
            return

        if isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
                return
            else:
                fmt = ' and '.join(missing)
            _message = 'I need the **{}** permission(s) to run this command.'.format(fmt)
            await ctx.respond(_message)
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.respond('This command has been disabled.')
            return

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond("This command is on cooldown, please retry in {}s.".format(math.ceil(error.retry_after)))
            return

        if isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
                return
            else:
                fmt = ' and '.join(missing)
            _message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
            await ctx.respond(_message)
            return

        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.respond('This command cannot be used in direct messages.')
            except discord.Forbidden:
                pass
            return
        if isinstance(error, discord.errors.NotFound):
            await ctx.author.respond("Internet error.")
        if isinstance(error, discord.errors.Forbidden):
                pass


def setup(bot):
    bot.add_cog(ErrorHandler(bot))