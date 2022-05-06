from __future__ import annotations

import discord
from discord.ext import commands

from ..aki import Akinator

class AkiView(discord.ui.View):

    def __init__(self, game: BetaAkinator, *, timeout: float) -> None:
        self.game = game
        super().__init__(timeout=timeout)

    async def process_input(self, interaction: discord.Interaction, answer: str) -> None:

        game = self.game
        
        if game.aki.progression >= game.win_at:
                embed = await game.win()
                await interaction.response.edit_message(embed=embed, view=self)
                if answer == "yes":
                    return self.stop()
        
        if interaction.user != game.player:
            return await interaction.response.send_message(content="This isn't your game")

        if answer == "Cancel":
            await interaction.response.edit_message(view=None)

        else:
            game.questions += 1
            await game.aki.answer(answer)

            embed = await game.build_embed()
            await interaction.response.edit_message(embed=embed, view=self)


    @discord.ui.button(label="yes", style=discord.ButtonStyle.green)
    async def yes_button(self, button: discord.Button, interaction: discord.Interaction):
        await self.process_input(interaction, "y")

    @discord.ui.button(label="no", style=discord.ButtonStyle.red)
    async def no_button(self, button: discord.Button, interaction: discord.Interaction):
        await self.process_input(interaction, "n")

    @discord.ui.button(label="idk", style=discord.ButtonStyle.blurple)
    async def idk_button(self, button: discord.Button, interaction: discord.Interaction):
        await self.process_input(interaction, "i")

    @discord.ui.button(label="probably", style=discord.ButtonStyle.grey)
    async def py_button(self, button: discord.Button, interaction: discord.Interaction):
        await self.process_input(interaction, "p")

    @discord.ui.button(label="probably not", style=discord.ButtonStyle.grey)
    async def pn_button(self, button: discord.Button, interaction: discord.Interaction):
        await self.process_input(interaction, "pn")

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, row=1)
    async def del_button(self, button: discord.Button, interaction: discord.Interaction):
        await self.process_input(interaction, "Cancel")
        

class BetaAkinator(Akinator):

    async def start(
        self, 
        ctx: commands.Context,
        *,
        win_at: int = 80, 
        timeout: int = None,
        child_mode: bool = True,
    ) -> None:

        self.player = ctx.author
        self.win_at = win_at
        self.view = AkiView(self, timeout=timeout)

        await self.aki.start_game(child_mode=child_mode)

        embed = await self.build_embed()
        self.message = await ctx.send(embed=embed, view=self.view)
