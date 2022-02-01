#pip install -U git+https://github.com/Pycord-Development/pycord ------ Keep this here

import discord
from discord.ext import commands

mention = commands.when_mentioned_or("b!")

intents = discord.Intents().all()
intents.members = True
case = True

token = "token" # bots token

banner = "" # bots profile avatar

delete = 5

# COLOUR HEX
hhelp = 0xffff33 #Help Embed
yellow = 0xffff00 #Regular Embeds
blue = 0x38B6FF #Dashboard Embeds

#OWNER CMDS
red = 0xed5757
green = 0x57f287 #Positive Events
owner = 0x5865f2
clear = 0x2f3136

#MOD ERROR
error = 0xed5757 #Negative Events

#LOGS
log = 0x87CEEB