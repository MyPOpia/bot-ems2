import discord
from discord.ext import commands
from discord import ui
from database import get_or_create_profile, update_profile, has_profile, create_profile

class RegisterView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="S'enregistrer", style=discord.ButtonStyle.green)
    async def register_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await has_profile(interaction.user.id):
            await interaction.response.send_message("❌ Vous êtes déjà enregistré.", ephemeral=True)
            return

        await interaction.response.send_modal(RegisterModal())

class RegisterModal(ui.Modal, title="Enregistrement EMS"):
    nom = ui.TextInput(label="Nom", placeholder="Ex: Dupont", required=True)
    prenom = ui.TextInput(label="Prénom", placeholder="Ex: Jean", required=True)
    user_id = ui.TextInput(label="ID Discord (copiez depuis votre profil)", placeholder="123456789012345678", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            discord_id = int(self.user_id.value)
        except ValueError:
            await interaction.response.send_message("❌ L'ID Discord doit être un nombre valide.", ephemeral=True)
            return

        if await has_profile(discord_id):
            await interaction.response.send_message("❌ Un profil avec cet ID existe déjà.", ephemeral=True)
            return

        await create_profile(discord_id, self.nom.value, self.prenom.value)
        await interaction.response.send_message("✅ Enregistrement effectué avec succès !", ephemeral=True)

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Profile(bot))
