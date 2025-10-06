import os
import discord
from discord.ext import commands

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    raise RuntimeError("Discord token is not set in the .env!")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="-", intents=intents)
bot.DISCORD_TOKEN = DISCORD_TOKEN

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

async def start_bot():
    await bot.load_extension("src.monitorcog")
    await bot.start(DISCORD_TOKEN)
