import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive
import asyncio
from db import init_storage

load_dotenv()

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

async def main():
    # Initialisation
    init_storage()
    keep_alive()

    # Chargement des cogs
    await bot.load_extension("cogs.events")
    await bot.load_extension("cogs.profile")
    await bot.load_extension("cogs.panel")
    await bot.load_extension("cogs.setup")

    # Démarrage du bot
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ Token manquant dans les variables d’environnement.")
        return

    await bot.start(token)

asyncio.run(main())

