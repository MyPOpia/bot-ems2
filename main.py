import os
import discord
from discord.ext import commands
from keep_alive import keep_alive
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


initial_extensions = [
    "cogs.events",
    "cogs.commands"
]

for ext in initial_extensions:
    try:
        bot.load_extension(ext)
        print(f"✅ Chargé : {ext}")
    except Exception as e:
        print(f"❌ Erreur de chargement {ext} : {e}")

keep_alive()

token = os.getenv("DISCORD_TOKEN")

if not token:
    print("❌ Erreur : La variable d'environnement DISCORD_TOKEN n'est pas définie.")
else:

    bot.load_extension("cogs.panel")

    bot.run(DISCORD_TOKEN)

