from __future__ import annotations

from typing import Optional

import discord
from discord.ext import commands

RED   = "<:Connect4Red:970935128039764029>"
BLUE  = "<:Connect4White:970935127989432350>"
BLANK = "<:Connect4Blank:970935128056549447>"

class ConnectFour:

    def __init__(self, *, red: discord.Member, blue: discord.Member):
        self.red_player  = red
        self.blue_player = blue

        self.board: list[list[str]] = [[BLANK for _ in range(7)] for _ in range(6)]
        self._controls: tuple[str] = ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣')

        self.turn = self.red_player
        self.message: Optional[discord.Message] = None
        self.winner: Optional[discord.Member] = None

        self._conversion: dict[str, int] = {
            '1️⃣': 0, 
            '2️⃣': 1, 
            '3️⃣': 2, 
            '4️⃣': 3, 
            '5️⃣': 4, 
            '6️⃣': 5, 
            '7️⃣': 6, 
        }
        self.player_to_emoji: dict[discord.Member, str]  = {
            self.red_player : RED, 
            self.blue_player: BLUE,
        }
        self.emoji_to_player: dict[str, discord.Member] = {
            RED: self.red_player, 
            BLUE: self.blue_player,
        }

    def board_string(self) -> str:
        board = "1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣\n"
        for row in self.board:
            board += "".join(row) + "\n"
        return board

    async def make_embed(self, *, status: bool) -> discord.Embed:
        embed = discord.Embed()
        if not status:
            embed.description = f"**Turn:** {self.turn.name}\n**Piece:** {self.player_to_emoji[self.turn]}"
        else:
            status_ = f"{self.winner} won!" if self.winner else "Tie"
            embed.description = f"**Game over**\n{status_}"
        return embed
        
    async def PlacePiece(self, emoji: str, user) -> list:
        
        if emoji not in self._controls:
            raise KeyError("Provided emoji is not one of the valid controls")
        y = self._conversion[emoji]

        for x in range(5, -1, -1):
            if self.board[x][y] == BLANK:
                self.board[x][y] = self.player_to_emoji[user]
                break

        self.turn = self.red_player if user == self.blue_player else self.blue_player
        return self.board

    async def is_game_over(self) -> bool:

        if all(i != BLANK for i in self.board[0]):
            return True

        for x in range(6):
            for i in range(4):
                if (self.board[x][i] == self.board[x][i+1] == self.board[x][i+2] == self.board[x][i+3]) and self.board[x][i] != BLANK:
                    self.winner = self.emoji_to_player[self.board[x][i]]
                    return True

        for x in range(3):
            for i in range(7):
                if (self.board[x][i] == self.board[x+1][i] == self.board[x+2][i] == self.board[x+3][i]) and self.board[x][i] != BLANK:
                    self.winner = self.emoji_to_player[self.board[x][i]]
                    return True

        for x in range(3):
            for i in range(4):
                if (self.board[x][i] == self.board[x + 1][i + 1] == self.board[x + 2][i + 2] == self.board[x + 3][i + 3]) and self.board[x][i] != BLANK:
                    self.winner = self.emoji_to_player[self.board[x][i]]
                    return True

        for x in range(5, 2, -1):
            for i in range(4):
                if (self.board[x][i] == self.board[x - 1][i + 1] == self.board[x - 2][i + 2] == self.board[x - 3][i + 3]) and self.board[x][i] != BLANK:
                    self.winner = self.emoji_to_player[self.board[x][i]]
                    return True

        return False
    
    async def start(self, ctx: commands.Context, *, remove_reaction_after: bool = False, **kwargs) -> discord.Message:

        embed = await self.make_embed(status=False)
        self.message = await ctx.send(self.board_string(), embed=embed, **kwargs)

        for button in self._controls:
            await self.message.add_reaction(button)

        while True:

            def check(reaction: discord.Reaction, user: discord.Member) -> bool:
                return (
                    str(reaction.emoji) in self._controls and 
                    user == self.turn and reaction.message == self.message and 
                    self.board[0][self._conversion[str(reaction.emoji)]] == BLANK
                )

            reaction, user = await ctx.bot.wait_for("reaction_add", check=check)

            emoji = str(reaction.emoji)
            await self.PlacePiece(emoji, user)

            if status := await self.is_game_over():
                break

            if remove_reaction_after:
                await self.message.remove_reaction(emoji, user)
                
            embed = await self.make_embed(status=False)
            await self.message.edit(content=self.board_string(), embed=embed)
        
        embed = await self.make_embed(status=status)
        return await self.message.edit(content=self.board_string(), embed=embed)