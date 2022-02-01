import discord
import json

from discord.ext import commands
from modules import bot as v

"""
leveling
leveling on/off: level
channel: lvlchannel

this is the database names for dash"""

class level(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:         
            with open('databases/levels.json','r') as f:
                users = json.load(f)
            
            await open_account(users, message.author, message.guild)
            await add_experience(users, message.author, 1, message.guild)
            await level_up(self, users, message.author, message.channel, message.guild)

            with open('databases/levels.json','w') as f:
                json.dump(users, f)

            return

    @commands.command()
    async def rank(self, ctx, member: discord.Member = None):
        if member == self.client.user:
            await ctx.send("I have no rank because I am a bot")
            return

        if not member:
            user = ctx.message.author
            
            with open('databases/levels.json','r') as f:
                users = json.load(f)
            
            lvl = users[str(ctx.guild.id)][str(user.id)]['level']
            exp = users[str(ctx.guild.id)][str(user.id)]['experience']

            embed = discord.Embed(title=f"**__{ctx.author.name}'s level__**", color=v.yellow)
            embed.set_thumbnail(url=ctx.author.avatar.url)
            embed.add_field(name="**__Level:__**", value=f"Level {lvl}", inline=True)
            embed.add_field(name="**__Experience:__**", value=f"{exp} XP", inline=True)
            embed.set_footer(text=f" |   {ctx.author.name}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            return

        else:
            with open('databases/levels.json','r') as f:
                users = json.load(f)
            
            lvl = users[str(ctx.guild.id)][str(member.id)]['level']
            exp = users[str(ctx.guild.id)][str(member.id)]['experience']
            

            embed = discord.Embed(title=f"**__{member.name}'s level__**", color=v.yellow)
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="**__Level:__**", value=f"Level {lvl}", inline=True)
            embed.add_field(name="**__Experience:__**", value=f"{exp} XP", inline=True)
            embed.set_footer(text=f" |   {ctx.author.name}", icon_url=ctx.author.avatar.url)

            await ctx.send(embed=embed)
            return

async def open_account(users, user, server):
    if not str(user.id) in users[str(server.id)]:
        users[str(server.id)][str(user.id)] = {}
        users[str(server.id)][str(user.id)]['level'] = 0
        users[str(server.id)][str(user.id)]['experience'] = 0

async def add_experience(users, user, exp, server):
    users[str(user.guild.id)][str(user.id)]['experience'] += exp

async def level_up(self, users, user, channel, server):
    
    experience = users[str(user.guild.id)][str(user.id)]['experience']
    lvl_end = int(experience ** (1/3))

    lvl_start = users[str(user.guild.id)][str(user.id)]['level']
    
    if lvl_start < lvl_end:
        users[str(user.guild.id)][str(user.id)]['level'] = lvl_end
    

    if lvl_start < lvl_end:

        player = user.mention
        lvl = users[str(user.guild.id)][str(user.id)]['level']

        mess = f"GG {player}, you just advanced to level {lvl}"

        channel = self.client.get_channel(int(000000)) #id of channel
        await channel.send(mess)

def setup(client):
    client.add_cog(level(client))