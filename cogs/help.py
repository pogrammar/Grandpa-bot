import discord
import random
from discord.ext import commands, pages


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pages = [
            discord.Embed(title="About", description="I am a bot made collaborative with <@503720029456695306>\nI am a grandad who is updated on the latest memes. I respond to dad bot and mom bot, and I also have some funcions of my own. See them by clicking the buttons!\n\n\n [Invite me!](https://discord.com/api/oauth2/authorize?client_id=957709454583947276&permissions=535260822592&scope=bot%20applications.commands) • [Discord server](https://discord.gg/RVMNP6TAGx)", color=discord.Color.random()),
            discord.Embed(title="Commands", description="Functions that are trigered when the prefix `~` is given.\n\n__**These are also availible in slash commands.**__", color=discord.Color.random()),
            discord.Embed(title="Guild Admin Commands", description="Functions that are only the mods/admins can execute `~` is given.\n\n__**These are also availible in slash commands.**__", color=discord.Color.random()),
            discord.Embed(title="Developer contact", description="Commands to send feedback to the developers.\n\n__**These are also availible in slash commands.**__", color=discord.Color.random()),
            discord.Embed(title="Privacy", description="The command to view our Privacy policy.\n\n__**These are also availible in slash commands.**__", color=discord.Color.random()),
            discord.Embed(title="Owner only", description="Commands that can only be executed by my owner.\n\n__**Every command except the status commands are availible in slash commands.**__", color=discord.Color.random()),
            
        ]
        self.pages[1].add_field(name="Dad jokes", value=f"Usage: `~joke`\nSends: `A dad joke`\ncooldown: `30 seconds`", inline=False)
        self.pages[1].add_field(name="Tic tac toe", value=f"Usage: `~tic`\nSends: `A tic tac toe game`\ncooldown: `30 seconds`", inline=False)
        self.pages[1].add_field(name="Rock paper scissors", value=f"Usage: `~rps`\nSends: `A Rock paper scissors game`\ncooldown: `30 seconds`", inline=False)
        self.pages[1].add_field(name="Dice roll", value=f"Usage: `~roll`\nSends: `A dice roll game`\ncooldown: `30 seconds`", inline=False)
        
        self.pages[2].add_field(name="Set prefix", value=f"Usage: `~setprefix <new_prefix>`\nChanges: `The server prefix`\ncooldown: `30 seconds`", inline=False)



        self.pages[3].add_field(name="Suggest", value=f"Usage: `~suggest`\nSends: `An input box to send the devs a suggestion.`", inline=False)
        self.pages[3].add_field(name="Feedback", value=f"Usage: `~feedback`\nSends: `An input box to send the devs feedback. Its valuable!`", inline=False)
        self.pages[3].add_field(name="Error report", value=f"Usage: `~report`\nSends: `An input box to send the devs a report for an error. Its valuable!`", inline=False)
        
        
        self.pages[4].add_field(name="privacy", value=f"Usage: `~privacy`\nSends: `Our privacy policy.`", inline=False)
        
        
        
        self.pages[5].add_field(name="Servers", value=f"Usage: `~servers`\nSends: `The count of the servers the bot is in.`", inline=False)
        self.pages[5].add_field(name="Ping", value=f"Usage: `~ping`\nSends: `The ping latency.`", inline=False)
        self.pages[5].add_field(name="Status", value=f"Usage: `~status online/idle/dnd <status message>`\nSends: `Changes the bot's status respectively.`", inline=False)

        
        

    def get_pages(self):
        return self.pages

    








    @commands.command()
    async def help(self, ctx):
        """I'm Always here for help!"""
        paginator = pages.Paginator(pages=self.get_pages(), use_default_buttons=False)
        paginator.add_button(pages.PaginatorButton("prev", label="<", style=discord.ButtonStyle.blurple))
        paginator.add_button(pages.PaginatorButton("page_indicator", style=discord.ButtonStyle.gray, disabled=True))
        paginator.add_button(pages.PaginatorButton("next", style=discord.ButtonStyle.blurple))
        await paginator.send(ctx)


def setup(bot):
    bot.add_cog(Help(bot))
        