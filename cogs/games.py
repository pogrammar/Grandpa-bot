import discord
from discord.ext import commands, bridge
from discord.ui import *
from typing import List
import random
import asyncio
from main import bot
import os
from .GameHandler import *
from main import tips, counter
from .GameHandler import hangman

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
            self.emoji = "<:X_:968012049957412925>"
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = "<:O_:968012050020307004>"
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
        """Starts a tic-tac-toe game."""
        await ctx.respond("Tic Tac Toe: X goes first", view=TicTacToe())
        counter += 1
        if counter % 5 == 0:
            await asyncio.sleep(1)
            await ctx.send(random.choice(tips))

    @bridge.bridge_command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def roll(self, ctx):
        """Rolls a dice... That's all."""
        message = await ctx.respond("Choose a number:\n**4**, **6**, **8**, **10**, **12**, **20** ")
        counter += 1
        if counter % 5 == 0:
            await asyncio.sleep(1)
            await ctx.send(random.choice(tips))
        
        def check(m):
            return m.author == ctx.author

        try:
            message = await self.bot.wait_for("message", check = check, timeout = 30.0)
            m = message.content

            if m != "4" and m != "6" and m != "8" and m != "10" and m != "12" and m != "20":
                await message.send("Sorry, invalid choice.")
                return
            
            await message.send(f"**{random.randint(1, int(m))}**")
        except asyncio.TimeoutError:
            await message.delete()
            await ctx.respond("Process has been canceled because you didn't respond in **30 seconds**")
            counter += 1
            if counter % 5 == 0:
                await asyncio.sleep(1)
                await ctx.send(random.choice(tips))

    
    @bridge.bridge_command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def hangman(self, ctx):
        """Starts a hangman game."""
        try:
            await hangman.play(self.bot, ctx)
            counter += 1
            if counter % 5 == 0:
                await asyncio.sleep(1)
                await ctx.send(random.choice(tips))
            print("Hangman game started")
        except Exception as e:
            print(e)
    
    @bridge.bridge_command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def rps(self, ctx):
        """Starts a rock-paper-scissors game."""
        await ctx.respond("Below:")
        game = BetaRockPaperScissors()
        await game.start(ctx)
        counter += 1
        if counter % 5 == 0:
            await asyncio.sleep(1)
            await ctx.send(random.choice(tips))

    @bridge.bridge_command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def toss(self, ctx):
        """Toss a coin."""
        coin = ['+ heads', '- tails']
        await ctx.respond(f"```diff\n{random.choice(coin)}\n```")
        counter += 1
        if counter % 5 == 0:
            await asyncio.sleep(1)
            await ctx.send(random.choice(tips))
    @bridge.bridge_command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def memory(self, ctx):
        await ctx.respond("Below:")
        """Start a memory-based match-the pair game."""
        try:
            print("Get MMemory Game")
            game = MemoryGame()
            print("Start Memory Game")
            await game.start(ctx)
            counter += 1
            if counter % 5 == 0:
                await asyncio.sleep(1)
                await ctx.send(random.choice(tips))
            print("Finished Memory game")
        except Exception as e:
            print(e)

    @bridge.bridge_command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def aki(self, ctx):
        """Start an akinator game."""
        try:
            
            await ctx.respond("Starting game...")
            game = Akinator()
            print("Get Akinator game")
            await game.start(ctx)   
            counter += 1
            if counter % 5 == 0:
                await asyncio.sleep(1)
                await ctx.send(random.choice(tips))
            print("Start akinator game")
        except Exception as e:
            print(e)

def setup(bot):
    bot.add_cog(Games(bot))
