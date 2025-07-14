# client.py

import discord
from discord.ext import commands

TOKEN = "MTM5NDMzMzgwNzk0NzAyNjQzMg.GY2Cec.Uv-gauTs_RjO8cPFd9fuynGohtWIEQVagbPrHw"
intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Le bot est connecté en tant que {bot.user}")

