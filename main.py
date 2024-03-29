import os
import discord
from discord.ext import bridge, commands
import config
import asyncpg
from discord_together import DiscordTogether
from discord.commands import Option
import random
from discord.ui import *
counter = 0
tips = [
  "You can join the [support server](https://discord.gg/vbmqkrUWJD) for the latest updates! https://discord.gg/vbmqkrUWJD",
  "Want exclusive-access to grandpa bot's beta features, become a patreon today! https://www.patreon.com/betchespy",
  "We have a giveaway going on in [support server](https://discord.gg/vbmqkrUWJD)! Check it out [here!](https://discord.com/channels/456542159210807307/976578984244555847/976579468300804136) ",
  "Patreons get verious perks! check them out here! https://www.patreon.com/betchespy",
]

DEFAULT_PREFIX = '~'


async def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(DEFAULT_PREFIX)(bot,message)

    prefix = await bot.db.fetch('SELECT prefix FROM guilds WHERE "guild_id" = $1', message.guild.id)
    if len(prefix) == 0:
        await bot.db.execute('INSERT INTO guilds("guild_id", prefix) VALUES ($1, $2)', message.guild.id, DEFAULT_PREFIX)
        prefix = DEFAULT_PREFIX
    else: 
        prefix = prefix[0].get("prefix")
    return commands.when_mentioned_or(prefix)(bot,message)

intents = discord.Intents.default()
intents.message_content = True
bot = bridge.Bot(command_prefix=get_prefix,
                   help_command=None, 
                   intents = intents,
                   activity=discord.Game("Starting up..."),
                   status=discord.Status.dnd, 
                   owner_id=734641452214124674,
                  )

async def create_db_pool():
    bot.db = await asyncpg.create_pool(dsn='My DsN oMg')
    print("pgAdmin Connection sucessfull")

for filename in os.listdir("./cogs"):
    if filename.endswith('.py'): 
        bot.load_extension(name=f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
    bot.togetherControl = await DiscordTogether(config.TOKEN)
    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Activity(
            type=discord.ActivityType.listening, name="the latest memes || ~help"
            )  
            )  
    print("Bot is ready!")
    print(' ')
    print(f"Curently connected to {len(bot.guilds)} servers!")
    for guild in bot.guilds:
        print(guild.name)
    
    
@bot.event
async def on_guild_join(guild: discord.Guild):
    print(f'Bot has been added to {guild.name}')

    textchannels = guild.text_channels
    channel = random.choice(textchannels)
    embed=discord.Embed(title="Hi, I'm grandpa bot!", description=f"Thank you for adding me! <3\nNote that I do not need any setup whatsoever.\n\nPrefix: `~`\nHelp command: `~help`\n\nCreated by: <@734641452214124674>", color=discord.Color.random())
    embed.set_footer(text="The use of this bot is in agreement of the privacy policy.")

    button = Button(label="Privacy Policy", url="https://github.com/pogrammar/Grandpa-bot/blob/master/PRIVACY.md")
    view = View(timeout=30)
    view.add_item(button)

    await channel.send(embed=embed, view=view)

@bot.event
async def on_guild_remove(guild):
    await bot.db.execute('DELETE from guilds("guild_id", prefix)')
    print(f'Bot has been kicked from {guild.name}')


@bot.bridge_command()
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def setprefix(ctx, *, new_prefix):
    await bot.db.execute('UPDATE guilds SET prefix = $1 WHERE "guild_id" = $2', new_prefix, ctx.guild.id)
    await ctx.respond(f"Server prefix changed to {new_prefix}")
    

@bot.bridge_command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def invite(ctx):
    await ctx.respond(f"Invite me: https://discord.com/api/oauth2/authorize?client_id=957709454583947276&permissions=535260822592&scope=bot%20applications.commands")    
    
@bot.bridge_command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def patreon(ctx):
    await ctx.respond(f"Become a patron: https://www.patreon.com/betchespy")    



@bot.slash_command(guild_ids=[953593619288301598, 456542159210807307])
@commands.cooldown(1, 30, commands.BucketType.user)
async def activity(
    ctx, 
    voice_channel: Option(discord.VoiceChannel, "The voice channel you want the activity in"),
    game: Option(str, "The type of game you want to play", choices=['youtube', 'poker', 'betrayal', 'fishing', 'chess', 'letter-league', 'word-snack', 'sketch-heads', 'spellcast', 'awkword', 'checkers', 'blazing-8s', 'land-io', 'putt-party', 'ask-away'])
    
    ):
    link = await bot.togetherControl.create_link(voice_channel.id, game)
    await ctx.respond(f"Click the blue link!\n{link}")












bot.loop.run_until_complete(create_db_pool())

bot.run(config.TOKEN)
