from socket import timeout
from tkinter import E
import discord
from discord.ext import commands, bridge
from discord.ui import *
import aiohttp



class JokeCog(commands.Cog):
    def __init__(self, bot):
        self.bot  = bot

    @bridge.bridge_command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def joke(self, ctx):
        """Jokes. Its self explanatory tbh"""
        
        class DadJokeButton(discord.ui.Button):
            def __init__(self):
                super().__init__(style=discord.ButtonStyle.green, label="Joke", disabled=False)
                view: DadJokeView()

            async def callback(self, interaction: discord.Interaction):
                api = 'https://icanhazdadjoke.com/'
                async with aiohttp.request('GET', api, headers={'Accept': 'text/plain'}) as r:
                    result = await r.text()
                    await interaction.response.edit_message(content=result) 
            
        class DadJokeView(View):
            def __init__(self):
                super().__init__(timeout=20.0)
                self.add_item(DadJokeButton())
            
            async def on_timeout(self):
                try:
                    self.disable_all_items() 
                    await msg.edit(view=self)
                except Exception as e:
                    print(e)


        msg = await ctx.respond("Click the button for some jokes!" , view=DadJokeView())

def setup(bot):
    bot.add_cog(JokeCog(bot))