import discord
import random
from discord.ext import commands, pages, bridge
from discord.ui import *

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.about_pages = [
            discord.Embed(title="About", description="I am a bot made collaborative with <@503720029456695306>\nI am a grandad who is updated on the latest memes. I respond to dad bot and mom bot, and I also have some funcions of my own. See them by clicking the buttons!\n\n\n [Invite me!](https://discord.com/api/oauth2/authorize?client_id=957709454583947276&permissions=535260822592&scope=bot%20applications.commands)   •   [Discord server](https://discord.gg/RVMNP6TAGx)   •   [Github](https://github.com/pogrammar/Grandpa-bot)   •   [Patreon](https://www.patreon.com/betchespy)", color=discord.Color.random()),
        ]




        self.command_pages = [
            discord.Embed(title="Commands", description="Functions that are trigered when the prefix `~` is given.\n\n__**These are also availible in slash commands.**__", color=discord.Color.random()),
            discord.Embed(title="Dad jokes", description=f"Usage: `~joke`\nSends: `A dad joke`\ncooldown: `30 seconds`", color=discord.Color.random()),
            discord.Embed(title="Games", description=f"In-Built fun games to play :)`", color=discord.Color.random()),
        ]
        self.command_pages[2].add_field(name="Tic tac toe", value=f"Usage: `~tic`\nSends: `A tic tac toe game`\ncooldown: `30 seconds`", inline=False)
        self.command_pages[2].add_field(name="Dice roll", value=f"Usage: `~roll`\nSends: `A dice roll game`\ncooldown: `30 seconds`", inline=False)


        self.guild_admin_command_pages = [
            discord.Embed(title="Guild Admin Commands", description="Functions that are only the mods/admins can execute `~` is given.\n\n__**These are also availible in slash commands.**__", color=discord.Color.random()),
        ]

        self.guild_admin_command_pages[0].add_field(name="Set prefix", value=f"Usage: `~setprefix <new_prefix>`\nChanges: `The server prefix`\ncooldown: `30 seconds`", inline=False)
        


        self.developer_contact_pages = [
            discord.Embed(title="Developer contact", description="Commands to send feedback to the developers.\n\n__**These are also availible in slash commands.**__", color=discord.Color.random()),
        
        ]
        self.developer_contact_pages[0].add_field(name="Suggest", value=f"Usage: `~suggest`\nSends: `An input box to send the devs a suggestion.`", inline=False)
        self.developer_contact_pages[0].add_field(name="Feedback", value=f"Usage: `~feedback`\nSends: `An input box to send the devs feedback. Its valuable!`", inline=False)
        self.developer_contact_pages[0].add_field(name="Error report", value=f"Usage: `~report`\nSends: `An input box to send the devs a report for an error. Its valuable!`", inline=False)


        self.privacy_pages = [
            discord.Embed(title="Privacy", description="The command to view our Privacy policy.\n\n__**These are also availible in slash commands.**__", color=discord.Color.random()),
     
        ]
        self.privacy_pages[0].add_field(name="privacy", value=f"Usage: `~privacy`\nSends: `Our privacy policy.`", inline=False)


        self.owner_pages = [
            discord.Embed(title="Owner only", description="Commands that can only be executed by my owner.\n\n__**Every command except the status commands are availible in slash commands.**__", color=discord.Color.random()),
        ]
        self.owner_pages[0].add_field(name="Servers", value=f"Usage: `~servers`\nSends: `The count of the servers the bot is in.`", inline=False)
        self.owner_pages[0].add_field(name="Ping", value=f"Usage: `~ping`\nSends: `The ping latency.`", inline=False)
        self.owner_pages[0].add_field(name="Status", value=f"Usage: `~status online/idle/dnd <status message>`\nSends: `Changes the bot's status respectively.`", inline=False)


    @commands.command()
    async def help(self, ctx):
        page_buttons_basic = [
            pages.PaginatorButton("prev", label="<-", style=discord.ButtonStyle.blurple),
            pages.PaginatorButton("page_indicator", style=discord.ButtonStyle.gray, disabled=True),
            pages.PaginatorButton("next", label="->", style=discord.ButtonStyle.blurple),
        ]

        page_buttons_advanced = [
            pages.PaginatorButton("first", label="First", style=discord.ButtonStyle.blurple),
            pages.PaginatorButton("prev", label="<-", style=discord.ButtonStyle.green),
            pages.PaginatorButton("page_indicator", style=discord.ButtonStyle.gray, disabled=True),
            pages.PaginatorButton("next", label="->", style=discord.ButtonStyle.green),
            pages.PaginatorButton("last", label="Last", style=discord.ButtonStyle.blurple),
        ]
        page_groups = [
            pages.PageGroup(
                pages=self.about_pages,
                label="About",
                description="About this bot.",
                use_default_buttons=False,
                custom_buttons=None,
                show_disabled=False,
            ),
            pages.PageGroup(
                pages=self.command_pages,
                label="Commands",
                description="General commands.",
                custom_buttons=page_buttons_advanced,
                use_default_buttons=False,
                show_disabled=False,
            ),
            pages.PageGroup(
                pages=self.guild_admin_command_pages,
                label="Server admin commands",
                description="Commands that only admins/mods can execute.",
                use_default_buttons=False,
                custom_buttons=None,
                show_disabled=False,
            ),
            pages.PageGroup(
                pages=self.privacy_pages,
                label="Privacy Policy",
                description="Our privacy policy commands",
                use_default_buttons=False,
                custom_buttons=None,
                show_disabled=False,
            ),
            pages.PageGroup(
                pages=self.owner_pages,
                label="Owner commands",
                description="Commands that only my owner can execute.",
                use_default_buttons=False,
                custom_buttons=None,
                show_disabled=False,
            ),
        ]
        paginator = pages.Paginator(pages=page_groups, show_menu=True)
        await paginator.send(ctx)

def setup(bot):
    bot.add_cog(Help(bot))
        
