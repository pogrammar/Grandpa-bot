import discord
from discord.ext import commands, bridge
from discord.ui import *
import aiohttp



class DadJokeButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.green, label="Joke", disabled=False)

    async def callback(self, interaction: discord.Interaction):
        api = 'https://icanhazdadjoke.com/'
        async with aiohttp.request('GET', api, headers={'Accept': 'text/plain'}) as r:
            result = await r.text()
            await interaction.response.edit_message(content=result) 

class JokeCog(commands.Cog):
    def __init__(self, bot):
        self.bot  = bot

    @bridge.bridge_command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def joke(self, ctx):
        """Jokes. Its self explanatory tbh"""
        view = discord.ui.View(timeout=10.0)
        view.add_item(DadJokeButton())

        await ctx.respond("Click the button for some jokes!" , view=view)

def setup(bot):
    bot.add_cog(JokeCog(bot))