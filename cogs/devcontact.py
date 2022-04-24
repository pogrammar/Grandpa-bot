import discord
from discord.ext import commands
from discord.ext import bridge
from discord.ui import *
from main import bot


class SuggestionModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="Suggestion title", placeholder="Suggestion title"))

        self.add_item(InputText(label="Suggestion", placeholder="Suggestion", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"New suggestion: {self.children[0].value}", description=self.children[1].value, color=discord.Color.random())      
        embed.set_footer(text=interaction.user)
        member = await bot.fetch_user(734641452214124674)
        await member.send(embed=embed)
        await interaction.response.send_message("Suggestion sent!")
        

class FeedbackModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="Title", placeholder="Title"))

        self.add_item(InputText(label="Description", placeholder="Description", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"Feedback: {self.children[0].value}", description=self.children[1].value, color=discord.Color.random())      
        embed.set_footer(text=interaction.user)
        member = await bot.fetch_user(734641452214124674)
        await member.send(embed=embed)
        await interaction.response.send_message("Feedback sent!")



class ReportModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="Report title", placeholder="Title"))

        self.add_item(InputText(label="Error Description", placeholder="Description", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"New error report: {self.children[0].value}", description=self.children[1].value, color=discord.Color.random())      
        embed.set_footer(text=interaction.user)
        member = await bot.fetch_user(734641452214124674)
        await member.send(embed=embed)
        await interaction.response.send_message("Report sent!")







class DevContactClassic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def suggest(self, ctx):
        """Suggest the devs something! It can be anything!"""
        class MyView(discord.ui.View):
            @discord.ui.button(label="Send suggestion!", style=discord.ButtonStyle.secondary, emoji="📜")
            async def button_callback(self, button, interaction):
                modal = SuggestionModal(title="Create a new suggestion")
                await interaction.response.send_modal(modal)
                
        view = MyView()
        await ctx.respond("Click the button to suggest!", view = MyView())
                
    @bridge.bridge_command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def feedback(self, ctx):
        """We would love to hear from you! Your feedback really helps us improve!"""
        class MyView(discord.ui.View):
            @discord.ui.button(label="Send feedback", style=discord.ButtonStyle.primary, emoji="❤️")
            async def button_callback(self, button, interaction):
                modal = FeedbackModal(title="Send feedback")
                await interaction.response.send_modal(modal)
        
        view = MyView()
        await ctx.respond("Click the button to send feedback!", view = MyView())
    
    @bridge.bridge_command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def report(self, ctx):
        """Report us an error."""
        class MyView(discord.ui.View):
            @discord.ui.button(label="Report an error", style=discord.ButtonStyle.danger, emoji="⚠️")
            async def button_callback(self, button, interaction):
                modal = ReportModal(title="Report an error")
                await interaction.response.send_modal(modal)
                 
        view = MyView()
        await ctx.respond("Click the button to a report!", view = MyView()) 
        
        
        
def setup(bot):
    bot.add_cog(DevContactClassic(bot))