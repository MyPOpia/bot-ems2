import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


for filename in os.listdir("./events"):
    if filename.endswith(".py"):
        bot.load_extension(f"events.{filename[:-3]}")

keep_alive()

token = os.getenv("DISCORD_TOKEN")
if not token:
    print("Erreur : La variable d'environnement DISCORD_TOKEN n'est pas définie.")
else:
    bot.run(token)
