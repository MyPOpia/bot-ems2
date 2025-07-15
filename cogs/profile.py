import discord
from discord.ext import commands
from discord import ui
from db import create_profile, has_profile, get_or_create_profile, format_minutes

class RegisterView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="S'enregistrer", style=discord.ButtonStyle.green)
    async def register_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await has_profile(interaction.user.id):
            await interaction.response.send_message("❌ Vous êtes déjà enregistré.", ephemeral=True)
            return

        modal = RegisterModal()
        await interaction.response.send_modal(modal)

class RegisterModal(ui.Modal, title="Enregistrement EMS"):
    nom = ui.TextInput(label="Nom", placeholder="Ex: Dupont")
    prenom = ui.TextInput(label="Prénom", placeholder="Ex: Jean")

    async def on_submit(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        await create_profile(user_id, str(self.nom), str(self.prenom))
        await interaction.response.send_message("✅ Enregistrement effectué avec succès !", ephemeral=True)

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="register_panel")
    async def register_panel(self, ctx):
        """Affiche le bouton pour s'enregistrer."""
        view = RegisterView()
        await ctx.send("Clique sur le bouton ci-dessous pour t'enregistrer :", view=view)

    @commands.command(name="profil")
    async def profil(self, ctx):
        """Affiche ton profil EMS."""
        if not await has_profile(ctx.author.id):
            await ctx.send("❌ Tu n'es pas encore enregistré. Utilise `!register_panel`.")
            return

        profile = get_or_create_profile(ctx.author.id)
        embed = discord.Embed(title="🩺 Profil EMS", color=discord.Color.blue())
        embed.add_field(name="Nom", value=profile.get("nom", "Inconnu"), inline=True)
        embed.add_field(name="Prénom", value=profile.get("prenom", "Inconnu"), inline=True)
        embed.add_field(name="ID Discord", value=profile.get("discord_id"), inline=True)
        embed.add_field(name="⏱️ Temps de service", value=format_minutes(profile.get("heures_service", 0)), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="profil_joueur")
    async def profil_joueur(self, ctx, membre: discord.Member):
        """Affiche le profil EMS d’un autre utilisateur."""
        if not await has_profile(membre.id):
            await ctx.send("❌ Ce joueur n'est pas encore enregistré.")
            return

        profile = get_or_create_profile(membre.id)
        embed = discord.Embed(title=f"🩺 Profil de {membre.display_name}", color=discord.Color.green())
        embed.add_field(name="Nom", value=profile.get("nom", "Inconnu"), inline=True)
        embed.add_field(name="Prénom", value=profile.get("prenom", "Inconnu"), inline=True)
        embed.add_field(name="ID Discord", value=profile.get("discord_id"), inline=True)
        embed.add_field(name="⏱️ Temps de service", value=format_minutes(profile.get("heures_service", 0)), inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Profile(bot))

