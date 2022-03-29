import discord, os

from discord.ext import commands

from modules import bot as v

client = commands.Bot(command_prefix=v.mention, intents = v.intents, case_insensitive=v.case)
client.remove_command("help")

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord')

    await client.change_presence(status=discord.Status.online)
    #await client.change_presence(status=discord.Status.idle, activity="Down for maintenance")
    #await client.change_presence(status=discord.Status.do_not_disturb, activity="Down for heavy maintenance")

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"bobcatbot.xyz"))

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

for filename in os.listdir("./cogs/bot"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.bot.{filename[:-3]}")

client.run(v.token)

# hello github