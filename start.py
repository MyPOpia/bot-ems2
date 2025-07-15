import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.all()  
bot = commands.Bot(command_prefix="!", intents=intents)

# Charger directement le module events s'il existe
try:
    bot.load_extension("events")
except Exception as e:
    print(f"Erreur lors du chargement de l'extension 'events': {e}")

keep_alive()

token = os.getenv("DISCORD_TOKEN")

if not token:
    print("Erreur : La variable d'environnement DISCORD_TOKEN n'est pas définie.")
else:
    bot.run(token)
