import discord
from discord.ext import commands
import json
import os

CONFIG_FILE = "data/config.json"

def save_config(data):
    os.makedirs("data", exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setup_fantome")
    @commands.has_permissions(administrator=True)
    async def setup_fantome(self, ctx):
        config = load_config()
        config["fantome_channel"] = ctx.channel.id
        save_config(config)
        await ctx.send(f"✅ Salon des appels fantômes configuré ici : {ctx.channel.mention}")

def get_fantome_channel_id():
    config = load_config()
    return config.get("fantome_channel")

async def setup(bot):
    await bot.add_cog(Setup(bot))
