import discord
from discord.ext import commands, bridge
from discord.ui import *
from typing import List
import random
import asyncio


class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        # A label is required, but we don't need one so a zero-width space is used
        # The row parameter tells the View which row to place the button under.
        # A View can only contain up to 5 rows -- each row can only have 5 buttons.
        # Since a Tic Tac Toe grid is 3x3 that means we have 3 rows and 3 columns.
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed
    # This is part of the "meat" of the game logic
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        self.disabled = True
        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "X won!"
            elif winner == view.O:
                content = "O won!"
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


# This is our actual board View
class TicTacToe(discord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons
    # This is not required
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner -- it is used by the TicTacToeButton
    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == -3:
                return self.X

            elif value == 3:
                return self.O
        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == -3:
            return self.X

        elif diag == 3:
            return self.O
        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        


    @bridge.bridge_command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def tic(self, ctx):
        """Starts a tic-tac-toe game with yourself."""
        await ctx.respond("Tic Tac Toe: X goes first", view=TicTacToe())

    @bridge.bridge_command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def rps(self, ctx):
        """Rock Paper Scissors game."""
        try:
            rpsEmbed = discord.Embed(color=random.randint(
                0, 0xffffff))
            rpsEmbed.add_field(name='Rock', value='\U0001faa8')
            rpsEmbed.add_field(name='Paper', value='\U0001f4dc')
            rpsEmbed.add_field(name='Scissors', value='\U00002702')
            rpsEmbed.set_footer(text='the message you will be deleted after 1 min')
            question_choose = await ctx.respond(embed=rpsEmbed)
            await question_choose.add_reaction('\U0001faa8')
            await question_choose.add_reaction('\U0001f4dc')
            await question_choose.add_reaction('\U00002702')
            reaction, user = await self.bot.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author and str(reaction.emoji), timeout=60)
            
            selects = [u'\U00002702', u'\U0001faa8', u'\U0001f4dc']
            
            bot_select = random.choice(selects)
            print(str(bot_select))
            
            user_select = str(reaction.emoji)
            print(str(user_select))
        
            if str(user_select) == str(bot_select):
                await question_choose.delete()
                
                if str(bot_select) == u'\U00002702':
                    choose_embed = discord.Embed(color=0x2ecc71)
                    choose_embed.add_field(
                        name='User Choose :bust_in_silhouette:', value=f'**{user_select}**', inline=True)
                    choose_embed.add_field(
                        name='Bot Choose :robot:', value=f'**{bot_select}**', inline=True)
                    choose_embed.set_author(
                        name='Tie', icon_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/209/anticlockwise-downwards-and-upwards-open-circle-arrows_1f504.png')
                    choose_embed.set_footer(
                        text=ctx.author.name, icon_url=ctx.author.avatar.url)
                    await ctx.respond(embed=choose_embed)
                
                elif str(bot_select) == u'\U0001faa8':
                    choose_embed = discord.Embed(color=0x2ecc71)
                    choose_embed.add_field(
                        name='User Choose :bust_in_silhouette:', value=f'**{user_select}**', inline=True)
                    choose_embed.add_field(
                        name='Bot Choose :robot:', value=f'**{bot_select}**', inline=True)
                    choose_embed.set_author(
                        name='Tie', icon_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/209/anticlockwise-downwards-and-upwards-open-circle-arrows_1f504.png')
                    choose_embed.set_footer(
                        text=ctx.author.name, icon_url=ctx.author.avatar.url)
                    await ctx.respond(embed=choose_embed)
                
                elif str(bot_select) == u'\U0001f4dc':
                    choose_embed = discord.Embed(color=0x2ecc71)
                    choose_embed.add_field(
                        name='User Choose :bust_in_silhouette:', value=f'**{user_select}**', inline=True)
                    choose_embed.add_field(
                        name='Bot Choose :robot:', value=f'**{bot_select}**', inline=True)
                    choose_embed.set_author(
                        name='Tie', icon_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/209/anticlockwise-downwards-and-upwards-open-circle-arrows_1f504.png')
                    choose_embed.set_footer(
                        text=ctx.author.name, icon_url=ctx.author.avatar.url)
                    await ctx.respond(embed=choose_embed)
            
            elif str(user_select) == u'\U0001faa8':
                await question_choose.delete()
                if str(bot_select) == u'\U00002702':
                    choose_embed = discord.Embed(color=0x2ecc71)
                    choose_embed.add_field(
                        name='User Choose :bust_in_silhouette:', value=f'**{user_select}**', inline=True)
                    choose_embed.add_field(
                        name='Bot Choose :robot:', value=f'**{bot_select}**', inline=True)
                    choose_embed.set_author(
                        name='You Win', icon_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/259/check-mark-button_2705.png')
                    choose_embed.set_footer(
                        text=ctx.author.name, icon_url=ctx.author.avatar.url)
                    await ctx.respond(embed=choose_embed)
                elif str(bot_select) == u'\U0001f4dc':
                    choose_embed = discord.Embed(color=0x2ecc71)
                    choose_embed.add_field(
                        name='User Choose :bust_in_silhouette:', value=f'**{user_select}**', inline=True)
                    choose_embed.add_field(
                        name='Bot Choose :robot:', value=f'**{bot_select}**', inline=True)
                    choose_embed.set_author(
                        name='You Lose', icon_url='https://images.emojiterra.com/mozilla/512px/274c.png')
                    choose_embed.set_footer(
                        text=ctx.author.name, icon_url=ctx.author.avatar.url)
                    await ctx.respond(embed=choose_embed)
            elif str(user_select) == u'\U0001f4dc':
                await question_choose.delete()
                if str(bot_select) == u'\U0001faa8':
                    choose_embed = discord.Embed(color=0x2ecc71)
                    choose_embed.add_field(
                        name='User Choose :bust_in_silhouette:', value=f'**{user_select}**', inline=True)
                    choose_embed.add_field(
                        name='Bot Choose :robot:', value=f'**{bot_select}**', inline=True)
                    choose_embed.set_author(
                        name='You Win', icon_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/259/check-mark-button_2705.png')
                    choose_embed.set_footer(
                        text=ctx.author.name, icon_url=ctx.author.avatar.url)
                    await ctx.respond(embed=choose_embed)
                elif str(bot_select) == u'\U00002702':
                    choose_embed = discord.Embed(color=0x2ecc71)
                    choose_embed.add_field(
                        name='User Choose :bust_in_silhouette:', value=f'**{user_select}**', inline=True)
                    choose_embed.add_field(
                        name='Bot Choose :robot:', value=f'**{bot_select}**', inline=True)
                    choose_embed.set_author(
                        name='You Lose', icon_url='https://images.emojiterra.com/mozilla/512px/274c.png')
                    choose_embed.set_footer(
                        text=ctx.author.name, icon_url=ctx.author.avatar.url)
                    await ctx.respond(embed=choose_embed)
            elif str(user_select) == u'\U00002702':
                await question_choose.delete()
                if str(bot_select) == u'\U0001faa8':
                    choose_embed = discord.Embed(color=0x2ecc71)
                    choose_embed.add_field(
                        name='User Choose :bust_in_silhouette:', value=f'**{user_select}**', inline=True)
                    choose_embed.add_field(
                        name='Bot Choose :robot:', value=f'**{bot_select}**', inline=True)
                    choose_embed.set_author(
                        name='You Lose', icon_url='https://images.emojiterra.com/mozilla/512px/274c.png')
                    choose_embed.set_footer(
                        text=ctx.author.name, icon_url=ctx.author.avatar.url)
                    await ctx.respond(embed=choose_embed)
                elif str(bot_select) == u'\U0001f4dc':
                    choose_embed = discord.Embed(color=0x2ecc71)
                    choose_embed.add_field(
                        name='User Choose :bust_in_silhouette:', value=f'**{user_select}**', inline=True)
                    choose_embed.add_field(
                        name='Bot Choose :robot:', value=f'**{bot_select}**', inline=True)
                    choose_embed.set_author(
                        name='You Win', icon_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/259/check-mark-button_2705.png')
                    choose_embed.set_footer(
                        text=ctx.author.name, icon_url=ctx.author.avatar.url)
                    await ctx.respond(embed=choose_embed)
        except asyncio.TimeoutError:
            timeout = await ctx.respond('The Time is end try again')
            await timeout.delete(delay=10)

    @bridge.bridge_command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def roll(self, ctx):
        """Rolls a dice... That's all."""
        message = await ctx.respond("Choose a number:\n**4**, **6**, **8**, **10**, **12**, **20** ")
        
        def check(m):
            return m.author == ctx.author

        try:
            message = await self.bot.wait_for("message", check = check, timeout = 30.0)
            m = message.content

            if m != "4" and m != "6" and m != "8" and m != "10" and m != "12" and m != "20":
                await ctx.respond("Sorry, invalid choice.")
                return
            
            await ctx.respond(f"**{random.randint(1, int(m))}**")
        except asyncio.TimeoutError:
            await message.delete()
            await ctx.respond("Process has been canceled because you didn't respond in **30 seconds**")

def setup(bot):
    bot.add_cog(Games(bot))
