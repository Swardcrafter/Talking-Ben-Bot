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


@bot.event
async def on_guild_join(guild):
    db[guild.id] = {
        "name": guild.name,
        "id": guild.id,
        "channels": {

        }
    }
    for channel in guild.channels:
        db[guild.id]["channels"][channel.id] = {
            "name": channel.name,
            "id": channel.id,
            "whitelisted": []
        }

    Save(db)

@bot.event
async def on_guild_channel_update(before, channel):
    if before.name != channel.name:
        db[channel.guild.id]["channels"][channel.id]["name"] = channel.name

    Save(db)

@bot.event
async def on_guild_remove(guild):
    del db[guild.id]

    Save(db)

@bot.event
async def on_guild_channel_create(channel):
    db[channel.guild.id]["channels"][channel.id] = {
        "name": channel.name,
        "id": channel.id,
        "whitelisted": []
    }

    Save(db)


@bot.event
async def on_guild_channel_delete(channel):
    del db[channel.guild.id]["channels"][channel.id]

    Save(db)


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





keep_alive()
bot.run(os.environ['TOKEN'])
