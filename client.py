
import os
import discord
from discord.ext import commands
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)
                     
@bot.event
async

