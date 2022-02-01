import discord
import json

from discord.ext import commands
from modules import bot as v

class welc(commands.Cog):
    def __init__(self, client):
        self.client = client    
	
    @commands.Cog.listener()
    async def on_member_join(self, member):
        chan = 0000000 #id of channel

        welcome = self.client.get_channel(int(chan))

        await welcome.send(f"**{member.mention}** has joined **{member.guild.name}**")
        return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        chan = 0000000 #id of channel

        welcome = self.client.get_channel(int(chan))

        await welcome.send(f"**{member.mention}** has left **{member.guild.name}**")
        return

def setup(client):
	client.add_cog(welc(client))