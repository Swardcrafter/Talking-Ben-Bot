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
            "whitelisted": {},
            "blacklist": {},
            "whiteliston": False
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
        "whitelisted": {},
        "blacklist": {},
        "whiteliston": False
    }

    Save(db)


@bot.event
async def on_guild_channel_delete(channel):
    del db[channel.guild.id]["channels"][channel.id]

    Save(db)

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself to avoid potential infinite loops
    if message.author == bot.user:
        return
    
    channel = message.channel
    channelId = channel.id
    
    if(db[message.guild.id]["channels"][channelId]["whiteliston"] == True):
        print(message.author.id in db[message.guild.id]["channels"][channelId]["whitelisted"])
        if(message.author.id not in db[message.guild.id]["channels"][channelId]["whitelisted"]):
            await message.delete()
            embed=discord.Embed(title=f"You are not whitelisted in this channel.", color=0x007063)
            embed.set_author(name="Whitelist")
            embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
            await message.author.send(embed=embed)
    if(message.author.id in db[message.guild.id]["channels"][channelId]["blacklist"]):
        await message.delete()
        embed=discord.Embed(title=f"You are blacklisted in this channel.", color=0x007063)
        embed.set_author(name="Blacklist")
        embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
        await message.author.send(embed=embed)

### Commands:

@bot.tree.command(name="help")
@app_commands.describe()
async def help(interaction: discord.Interaction):
    embed=discord.Embed(title="Whitelists & Blacklists Commands:")
    embed.add_field(name="General Commands:", value="1. /viewlists | Sees who is in the whitelist and blacklist.\n2. /help | Shows this message.", inline=False)
    embed.add_field(name="Whitelist Commands:", value="1. /whiteliston | Turns on the whitelist in the channel used so that only whitelisted users can type in there. Only works if the whitelist is off. Only works if there is at least 1 person whitelisted. Can only be used by whitelisted users.\n2. /whitelistoff | Turns off the whitelist in the channel used so that anyone can type in there. Only works if the whitelist is on. Can only be used by whitelisted users.\n3. /addwhitelist [user] | Adds a user to the whitelist. If the whitelist is off and no users whitelisted, any admin can use it (may instead use a whitelist role). If whitelist is on or there are users whitelisted, can only be used by whitelisted users.\n4. /removewhitelist [user] | Removes a user from the whitelist. If there are users whitelisted they are the only people who can use this. If not, can't be used. If it makes there be no whitelisted users, it also turns off the whitelist.", inline=False)
    embed.add_field(name="Blacklist Commands:", value="1. /addblacklist [user] | Adds a user to the blacklist. Can only be used by admins if there arent any whitelisted users, if there are, can only be used by them.\n2. /removeblacklist [user] | Removes a user from the blacklist. Can only be used by admins if there aren't any whitelisted users, if there are, can only be used by them.", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="whiteliston")
@app_commands.describe()
async def whiteliston(interaction: discord.Interaction):
    channel = interaction.channel
    channelId = channel.id

    if(db[interaction.guild.id]["channels"][channelId]["whitelisted"] == {}):
        embed=discord.Embed(title=f"No users whitelisted, use /addwhitelist", color=0x007063)
        embed.set_author(name="Whitelist")
        embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        if(db[interaction.guild.id]["channels"][channelId]["whiteliston"] == False):
            if(interaction.user.id in db[interaction.guild.id]["channels"][channelId]["whitelisted"]):
                db[interaction.guild.id]["channels"][channelId]["whiteliston"] = True
                embed=discord.Embed(title=f"Turned the whitelist on.", color=0x007063)
                embed.set_author(name="Whitelist")
                embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed=discord.Embed(title=f"You must be whitelisted to run this command.", color=0x007063)
                embed.set_author(name="Whitelist")
                embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed=discord.Embed(title=f"Whitelist already on.", color=0x007063)
            embed.set_author(name="Whitelist")
            embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
            await interaction.response.send_message(embed=embed, ephemeral=True)


    Save(db)

@bot.tree.command(name="whitelistoff")
@app_commands.describe()
async def whitelistoff(interaction: discord.Interaction,):
    channel = interaction.channel
    channelId = channel.id

    if(db[interaction.guild.id]["channels"][channelId]["whitelisted"] == {}):
        embed=discord.Embed(title=f"No users whitelisted, use /addwhitelist", color=0x007063)
        embed.set_author(name="Whitelist")
        embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        if(db[interaction.guild.id]["channels"][channelId]["whiteliston"] == True):
            if(interaction.user.id in db[interaction.guild.id]["channels"][channelId]["whitelisted"]):
                db[interaction.guild.id]["channels"][channelId]["whiteliston"] = False
                embed=discord.Embed(title=f"Turned the whitelist off.", color=0x007063)
                embed.set_author(name="Whitelist")
                embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed=discord.Embed(title=f"You must be whitelisted to run this command.", color=0x007063)
                embed.set_author(name="Whitelist")
                embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed=discord.Embed(title=f"Whitelist already off.", color=0x007063)
            embed.set_author(name="Whitelist")
            embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    Save(db)



@bot.tree.command(name="addwhitelist")
@app_commands.describe(user="The user you want to add to the whitelist")
async def addwhitelist(interaction: discord.Interaction, user: discord.Member):
    channel = interaction.channel
    channelId = channel.id
	


    if(db[interaction.guild.id]["channels"][channelId]["whitelisted"] == {}):
        if(interaction.user.guild_permissions.administrator):
            db[interaction.guild.id]["channels"][channelId]["whitelisted"][user.id] = {
                "name": user.name,
                "id": user.id
            }
            embed=discord.Embed(title=f"Added {user.name} to whitelist", color=0x007063)
            embed.set_author(name="Whitelist")
            embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed=discord.Embed(title=f"You don't have the necissary permissions to run this. (Must have Administrator.)", color=0x007063)
            embed.set_author(name="Whitelist")
            embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        if(interaction.user.id in db[interaction.guild.id]["channels"][channelId]["whitelisted"]):
            db[interaction.guild.id]["channels"][channelId]["whitelisted"][user.id] = {
                "name": user.name,
                "id": user.id
            }
            embed=discord.Embed(title=f"Added {user.name} to whitelist", color=0x007063)
            embed.set_author(name="Whitelist")
            embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed=discord.Embed(title=f"You must be whitelisted to run this command while users are whitelisted.", color=0x007063)
            embed.set_author(name="Whitelist")
            embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            

    Save(db)

@bot.tree.command(name="removewhitelist")
@app_commands.describe(user="The user you want to remove from the whitelist")
async def removewhitelist(interaction: discord.Interaction, user: discord.Member):
    channel = interaction.channel
    channelId = channel.id

    if(db[interaction.guild.id]["channels"][channelId]["whitelisted"] == {}):
        if(interaction.user.guild_permissions.administrator):
            if(user.id in db[interaction.guild.id]["channels"][channelId]["whitelisted"]):
                del db[interaction.guild.id]["channels"][channelId]["whitelisted"][user.id]
                embed=discord.Embed(title=f"Removed {user.name} from whitelist", color=0x007063)
                embed.set_author(name="Whitelist")
                embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed=discord.Embed(title=f"{user.name} isn't whitelisted here", color=0x007063)
                embed.set_author(name="Whitelist")
                embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed=discord.Embed(title=f"You don't have the necissary permissions to run this. (Must have Administrator.)", color=0x007063)
            embed.set_author(name="Whitelist")
            embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        if(interaction.user.id in db[interaction.guild.id]["channels"][channelId]["whitelisted"]):
            if(user.id in db[interaction.guild.id]["channels"][channelId]["whitelisted"]):
                del db[interaction.guild.id]["channels"][channelId]["whitelisted"][user.id]
                embed=discord.Embed(title=f"Removed {user.name} from whitelist", color=0x007063)
                embed.set_author(name="Whitelist")
                embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed=discord.Embed(title=f"{user.name} isn't whitelisted here", color=0x007063)
                embed.set_author(name="Whitelist")
                embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed=discord.Embed(title=f"You must be whitelisted to run this command while users are whitelisted.", color=0x007063)
            embed.set_author(name="Whitelist")
            embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    Save(db)

@bot.tree.command(name="viewlists")
@app_commands.describe()
async def viewlists(interaction: discord.Interaction):
    channel = interaction.channel
    channelId = channel.id
    whitelisted = db[interaction.guild.id]["channels"][channelId]["whitelisted"]
    message = ""
    for userId in whitelisted:
        message += "    - " + whitelisted[userId]["name"] + "\n"
    embed=discord.Embed(title=f"Whitelisted Users in {interaction.channel.name}:", description=message, color=0x007063)
    embed.set_author(name="Whitelist")
    embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
    await interaction.user.send(embed=embed)
    channel = interaction.channel
    channelId = channel.id
    blacklisted = db[interaction.guild.id]["channels"][channelId]["blacklist"]
    message = ""
    for userId in blacklisted:
        message += "    - " + blacklisted[userId]["name"] + "\n"
    embed=discord.Embed(title=f"Blacklisted Users in {interaction.channel.name}:", description=message, color=0x007063)
    embed.set_author(name="Blacklist")
    embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
    await interaction.user.send(embed=embed)
    await interaction.response.send_message("Sent the information is dms.", ephemeral=True)



@bot.tree.command(name="addblacklist")
@app_commands.describe(user="The user you want to add to the blacklist")
async def addblacklist(interaction: discord.Interaction, user: discord.Member):
    channel = interaction.channel
    channelId = channel.id
	

    if(db[interaction.guild.id]["channels"][channelId]["whitelisted"] == {}):
        if(interaction.user.guild_permissions.administrator):
            db[interaction.guild.id]["channels"][channelId]["blacklist"][user.id] = {
                "name": user.name,
                "id": user.id
            }
            embed=discord.Embed(title=f"Added {user.name} to blacklist", color=0x007063)
            embed.set_author(name="Blacklist")
            embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed=discord.Embed(title=f"You don't have the necissary permissions to run this. (Must have Administrator.)", color=0x007063)
            embed.set_author(name="Blacklist")
            embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        if(interaction.user.id in db[interaction.guild.id]["channels"][channelId]["whitelisted"]):
            db[interaction.guild.id]["channels"][channelId]["blacklist"][user.id] = {
                "name": user.name,
                "id": user.id
            }
            embed=discord.Embed(title=f"Added {user.name} to blacklist", color=0x007063)
            embed.set_author(name="blacklist")
            embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed=discord.Embed(title=f"You must be whitelisted to run this command while users are whitelisted.", color=0x007063)
            embed.set_author(name="Blacklist")
            embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            

    Save(db)

@bot.tree.command(name="removeblacklist")
@app_commands.describe(user="The user you want to remove from the blacklist")
async def removeblacklist(interaction: discord.Interaction, user: discord.Member):
    channel = interaction.channel
    channelId = channel.id

    if(db[interaction.guild.id]["channels"][channelId]["whitelisted"] == {}):
        if(interaction.user.guild_permissions.administrator):
            if(user.id in db[interaction.guild.id]["channels"][channelId]["blacklist"]):
                del db[interaction.guild.id]["channels"][channelId]["blacklist"][user.id]
                embed=discord.Embed(title=f"Removed {user.name} from blacklist", color=0x007063)
                embed.set_author(name="Blacklist")
                embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed=discord.Embed(title=f"{user.name} isn't blacklisted here", color=0x007063)
                embed.set_author(name="Blacklist")
                embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed=discord.Embed(title=f"You don't have the necissary permissions to run this. (Must have Administrator.)", color=0x007063)
            embed.set_author(name="Blacklist")
            embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        if(interaction.user.id in db[interaction.guild.id]["channels"][channelId]["whitelisted"]):
            if(user.id in db[interaction.guild.id]["channels"][channelId]["blacklist"]):
                del db[interaction.guild.id]["channels"][channelId]["blacklist"][user.id]
                embed=discord.Embed(title=f"Removed {user.name} from blacklist", color=0x007063)
                embed.set_author(name="Blacklist")
                embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed=discord.Embed(title=f"{user.name} isn't blacklisted here", color=0x007063)
                embed.set_author(name="Blacklist")
                embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed=discord.Embed(title=f"You must be whitelisted to run this command while users are whitelisted.", color=0x007063)
            embed.set_author(name="Blacklist")
            embed.set_footer(text="- Whitelist Bot (Made by PlotTwist)")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            

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
