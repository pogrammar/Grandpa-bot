import discord
from discord.ext import commands, bridge
from discord.ui import *
from main import tips, counter, get_cooldown
import random
from discord.commands import cooldown
import asyncio


class CustomCooldown:
    def __init__(self, rate: int, per: float, alter_rate: int, alter_per: float, bucket: commands.BucketType, *, elements):

        intElementArray = []
        for element in elements:
          
          intElementArray.append(int(element))
        self.elements = intElementArray
        self.default_mapping = commands.CooldownMapping.from_cooldown(rate, per, bucket)
        self.altered_mapping = commands.CooldownMapping.from_cooldown(alter_rate, alter_per, bucket)

    def __call__(self, ctx: commands.Context):
        key = self.altered_mapping._bucket_key(ctx.message)
        if key in self.elements:
            bucket = self.altered_mapping.get_bucket(ctx.message)
        else:
            bucket = self.default_mapping.get_bucket(ctx.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            raise commands.CommandOnCooldown(bucket, retry_after)
        return True






class Privacy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command()
    @commands.check(CustomCooldown(ctx=privacy.ctx))
    async def privacy(self, ctx):
        """Our terms on privacy."""
        embed = discord.Embed(title="Our terms on privacy.", description="Its listed in the embed, Or you can view it by clicking the button below.")
        embed.add_field(name="Privacy Policy", value='The use of this application ("Bot") in a guild requires the collection of some specific user data ("Data"). The Data collected includes, but is limited to Discord guild ID values. Use of the Bot is considered an agreement to the terms of this Policy.', inline=True)
        
        embed.add_field(name="Access to data", value="Access to Data is only permitted to Bot's developers, and only in the scope required for the development, testing, and implementation of features for Bot. Data is not sold, provided to, or shared with any third party, except where required by law or a Terms of Service agreement. You can view the data upon request from <@734641452214124674>.", inline=False)
        
        embed.add_field(name="Storage of Data", value="So first of all, idc about your data.\nsecond of all, Data is stored in a PostgreSQL database. The database is secured to prevent external access, however no guarantee is provided and the Bot owners assume no liability for the unintentional or malicious breach of Data. In the event of an unauthorised Data access, users will be notified through the Discord client application.", inline=False)
        
        embed.add_field(name="User Rights", value="At any time, you have the right to request to view the Data pertaining to your Discord account. You may submit a request through the [Discord server](https://discord.gg/RVMNP6TAGx). You have the right to request the removal of relevant Data.", inline=False)
        
        
        embed.add_field(name="Underage Users", value="The use of the Bot is not permitted for minors under the age of 13, or under the age of legal consent for their country. This is in compliance with the [Discord Terms Of Service](https://discord.com/terms). No information will be knowingly stored from an underage user. If it is found out that a user is underage we will take all necessary action to delete the stored data.", inline=False)
        
        embed.add_field(name="Questions", value="If you have any questions or are concerned about what data might be being stored from your account contact <@734641452214124674>. For more information check the [Discord Terms Of Service](https://discord.com/terms).", inline=False)
        
        
        
        
        embed.set_footer(text="If any Questions, use the commands for developer contact")
        
        button = Button(label="Privacy Policy", url="hhttps://github.com/pogrammar/Grandpa-bot/blob/master/PRIVACY.md")
        view = View(timeout=30)
        view.add_item(button)
        cooldown(1, get_cooldown(user=ctx.author.id), commands.BucketType.user)
        await ctx.respond(embed=embed, view=view)
        counter += 1
        if counter % 5 == 0:
            await asyncio.sleep(1)
            await ctx.send(random.choice(tips))


def setup(bot):
    bot.add_cog(Privacy(bot))