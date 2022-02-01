import discord

from discord.ext import commands

class ai(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    #@commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.mentions[0] == self.client.user:
                embed = discord.Embed(title="", color=0xffff00)
                embed.add_field(name=f"Hey :wave:", value=f"I'm BobCat Commands\n The prefix on this server is: b! \nUse `b!help` for a list of commands", inline=True)
                await message.channel.send(embed=embed, delete_after=3.0)
        except:
            pass

def setup(client):
    client.add_cog(ai(client))