import discord
from discord import app_commands
from discord.ext import commands
import os
from keep_alive import keep_alive
from db import Save
from data import db

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Logged in.")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


'''


Example Command:


@bot.tree.command(name="setinfo")
@app_commands.describe(id="Id for this info", message="The message")
async def setInfo(interaction: discord.Interaction, id: int, message: str):
    if interaction.user.guild_permissions.administrator:
        if (id not in db.keys()):
            db[id] = message
            await interaction.response.send_message(
                f"You have set the /info with the id of {id} to {message}",
                ephemeral=True)
            Save(db)
        else:
            await interaction.response.send_message(
                f"This is already an info, to edit it, do /editInfo",
                ephemeral=True)
    else:
        await interaction.response.send_message(
            f"You don't have the perms to do this.", ephemeral=True)
'''




@bot.tree.command(name="setprefix")
@app_commands.describe(prefix="New Prefix.")
async def prefix(interaction: discord.Interaction, prefix: str):
    global db
    if (interaction.user.guild_permissions.administrator):
        bot.command_prefix = prefix
        await interaction.response.send_message(
            f"Set Prefix to: {bot.command_prefix}")



keep_alive()
bot.run(os.environ['TOKEN'])
