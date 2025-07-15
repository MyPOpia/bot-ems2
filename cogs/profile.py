import discord
from discord.ext import commands
from discord import ui
from db import create_profile, has_profile

class RegisterView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="S'enregistrer", style=discord.ButtonStyle.green)
    async def register_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await has_profile(interaction.user.id):
            await interaction.response.send_message("❌ Tu es déjà enregistré.", ephemeral=True)
            return

        modal = RegisterModal()
        await interaction.response.send_modal(modal)

class RegisterModal(ui.Modal, title="Enregistrement EMS"):
    nom = ui.TextInput(label="Nom", placeholder="Ex: Dupont", required=True)
    prenom = ui.TextInput(label="Prénom", placeholder="Ex: Jean", required=True)
    discord_id_jeu = ui.TextInput(label="ID Discord (en jeu)", placeholder="Ex: EMS123", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        await create_profile(
            user_id,
            nom=str(self.nom),
            prenom=str(self.prenom),
            discord_id=str(self.discord_id_jeu)
        )
        await interaction.response.send_message("✅ Enregistrement effectué avec succès !", ephemeral=True)

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="register_panel")
    async def register_panel(self, ctx):
        """Affiche le bouton pour s'enregistrer."""
        view = RegisterView()
        await ctx.send("Clique sur le bouton ci-dessous pour t'enregistrer :", view=view)

async def setup(bot):
    await bot.add_cog(Profile(bot))
