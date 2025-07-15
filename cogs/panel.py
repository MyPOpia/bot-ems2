import discord
from discord.ext import commands
from discord.ui import View, Button, Select
from db import get_or_create_profile, update_profile, has_profile, create_profile
import time

class PanelView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(StartServiceButton())
        self.add_item(StopServiceButton())
        self.add_item(SelectMenu())
        self.add_item(RegisterButton())

class StartServiceButton(Button):
    def __init__(self):
        super().__init__(label="🟢 Démarrer Service", style=discord.ButtonStyle.green)

    async def callback(self, interaction: discord.Interaction):
        if not await has_profile(interaction.user.id):
            await interaction.response.send_message("❌ Tu dois d'abord t'enregistrer via le bouton 'S'enregistrer'.", ephemeral=True)
            return

        user_id = interaction.user.id
        profile = get_or_create_profile(user_id)
        profile["__start_time"] = interaction.created_at.timestamp()
        update_profile(user_id, profile)
        await interaction.response.send_message("⏱️ Service démarré !", ephemeral=True)

class StopServiceButton(Button):
    def __init__(self):
        super().__init__(label="🔴 Arrêter Service", style=discord.ButtonStyle.red)

    async def callback(self, interaction: discord.Interaction):
        if not await has_profile(interaction.user.id):
            await interaction.response.send_message("❌ Tu dois d'abord t'enregistrer via le bouton 'S'enregistrer'.", ephemeral=True)
            return

        user_id = interaction.user.id
        profile = get_or_create_profile(user_id)
        if "__start_time" not in profile:
            await interaction.response.send_message("❌ Aucun service en cours.", ephemeral=True)
            return

        elapsed = interaction.created_at.timestamp() - profile["__start_time"]
        profile["heures_service"] += round(elapsed, 2)  # secondes totales
        del profile["__start_time"]
        update_profile(user_id, profile)

        heures = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        secondes = int(elapsed % 60)

        await interaction.response.send_message(
            f"⏹️ Service arrêté. Temps ajouté : {heures}h {minutes}min {secondes}s",
            ephemeral=True
        )

class RegisterButton(Button):
    def __init__(self):
        super().__init__(label="📝 S'enregistrer", style=discord.ButtonStyle.blurple)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(RegisterModal())

class RegisterModal(discord.ui.Modal, title="Enregistrement EMS"):
    nom = discord.ui.TextInput(label="Nom", required=True)
    prenom = discord.ui.TextInput(label="Prénom", required=True)
    discord_id = discord.ui.TextInput(label="ID Discord (ex: 123456789012345678)", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            user_id = int(self.discord_id.value.strip())
        except ValueError:
            await interaction.response.send_message("❌ L'ID Discord doit être un nombre.", ephemeral=True)
            return

        if await has_profile(user_id):
            await interaction.response.send_message("❌ Cet ID est déjà enregistré.", ephemeral=True)
            return

        await create_profile(user_id, self.nom.value, self.prenom.value)
        await interaction.response.send_message("✅ Enregistrement effectué avec succès !", ephemeral=True)

class SelectMenu(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Ajouter Réanimation", value="rea"),
            discord.SelectOption(label="Ajouter Soin", value="soin"),
            discord.SelectOption(label="Déclarer une absence", value="absence")
        ]
        super().__init__(placeholder="📋 Choisir une action", options=options)

    async def callback(self, interaction: discord.Interaction):
        if not await has_profile(interaction.user.id):
            await interaction.response.send_message("❌ Tu dois d'abord t'enregistrer via le bouton 'S'enregistrer'.", ephemeral=True)
            return

        if self.values[0] == "rea":
            await interaction.response.send_message("🔄 Fonction réa à venir", ephemeral=True)
        elif self.values[0] == "soin":
            await interaction.response.send_message("💉 Fonction soin à venir", ephemeral=True)
        elif self.values[0] == "absence":
            await interaction.response.send_message("📅 Fonction absence à venir", ephemeral=True)

class Panel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_called = {}

    @commands.command(name="panel")
    async def panel(self, ctx):
        now = time.time()
        user_id = ctx.author.id

        # Anti double appel rapide (2 secondes de délai)
        if user_id in self.last_called and now - self.last_called[user_id] < 2:
            return

        self.last_called[user_id] = now
        await ctx.send("📋 **Panel EMS**", view=PanelView())

async def setup(bot):
    await bot.add_cog(Panel(bot))
