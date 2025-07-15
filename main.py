import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive
import asyncio
from db import init_storage  # ✅ Ajouté ici

load_dotenv()

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

async def main():
    await bot.load_extension("cogs.events")
    await bot.load_extension("cogs.profile")
    await bot.load_extension("cogs.panel")

    init_storage()  # ✅ Crée le fichier JSON au besoin
    keep_alive()

    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ Token manquant dans les variables d’environnement.")
        return

    await bot.start(token)

asyncio.run(main())
