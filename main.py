import discord
from discord import app_commands
from discord.ext import commands
import os
from keep_alive import keep_alive
import asyncio

bot = commands.Bot(command_prefix="^_-", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Logged in.")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


keep_alive()
bot.run(os.environ['TOKEN'])
