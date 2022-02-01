import discord
from discord.ext import commands
from modules import bot as v

class server(commands.Cog):
    def __init__(self, client):
        self.client = client

    #membercount, servericon, serverbanner, serverinfo, roleinfo

    @commands.command()
    async def membercount(self, ctx):
        embed = discord.Embed(title=f"There are {str(ctx.guild.member_count)} members!", colour=v.yellow)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=["sicon", "guildicon"])
    async def servericon(self, ctx):
        if not ctx.guild.icon.url:
            embed = discord.Embed(title="Your server icon", color=v.yellow)
            embed.set_image(url="https://cdn.discordapp.com/attachments/896078844921016340/909788234500952064/logo.png")
            await ctx.send(embed=embed)
            return
            
        else:
            sicon_Embed = discord.Embed(title="Your server icon", color=v.yellow)
            sicon_Embed.set_image(url=ctx.guild.icon.url)
            await ctx.send(embed=sicon_Embed)

    @commands.command()
    async def serverbanner(self, ctx):
        if not ctx.guild.banner:
            embed = discord.Embed(title="Your server bannner", color=v.yellow)
            embed.set_image(url="https://cdn.discordapp.com/attachments/896078844921016340/909786071355764766/banner.png")
            await ctx.send(embed=embed)
            return

        else:
            embed = discord.Embed(title="Your server bannner", color=v.yellow, timestamp=ctx.message.created_at)
            embed.set_image(url=ctx.guild.banner)
            await ctx.send(embed=embed)
		
    @commands.command(aliases=["serverinfo", "server-info", "serverinformation", "guildinfo", "si", "gi"])
    async def sinfo(self, ctx):
        embed = discord.Embed(title=f"Server info | {ctx.guild.name}", color=v.yellow, timestamp=ctx.message.created_at)

        embed.set_thumbnail(url=ctx.guild.icon.url)

        embed.add_field(name="<:owner:912319195683889192> Owner", value=f"{ctx.guild.owner.mention}", inline=False)
        embed.add_field(name="<:ID:912319260875960360> ID", value=f"`{ctx.guild.id}`", inline=False)
        embed.add_field(name="<:region:912331481802743818> Region", value=f"`{ctx.guild.region}`", inline=False)
        embed.add_field(name="<:members:912319097235202068> Members", value=f"`{len(list(filter(lambda m: m.bot, ctx.guild.members)))}`", inline=False)
        embed.add_field(name="<:bot:912319795372904458> Bots", value=f"`{len(list(filter(lambda m: m.bot, ctx.guild.members)))}`", inline=False)
        embed.add_field(name="<:text:912320257698439170> Text channels", value=f"`{len(ctx.guild.text_channels)}`", inline=False)
        embed.add_field(name="<:voice:912320372395900978> Voice channels", value=f"`{len(ctx.guild.voice_channels)}`", inline=False)
        embed.add_field(name="<:cats:912320462552453140> Categories", value=f"`{len(ctx.guild.categories)}`", inline=False)
        embed.add_field(name="<:flag:912327154296061992> Roles", value=f"`{len(ctx.guild.roles)}`", inline=False)
        embed.add_field(name="<:bot:912319795372904458> Server icon", value= f"[Icon]({ctx.guild.icon.url})", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def roleinfo(self, ctx, role : discord.Role):
        perm_list = [perm[0] for perm in role.permissions if perm[1]]
        role = role.created_at.strftime("%d/%m/%Y %H:%M:%S")

        embed = discord.Embed(color=v.yellow)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.add_field(name=f"<:members:912319097235202068> Role Name", value=f"`{role}`", inline=False)
        embed.add_field(name=f"<:ID:912319260875960360> Role ID", value=f"`{role.id}`", inline=False)
        embed.add_field(name=f"<:text:912320257698439170> Role Mention", value=f"{role.mention}", inline=False)
        embed.add_field(name=f"<:moderation:912319464572334140> Role Permissions", value=f"`{perm_list}`", inline=False)
        embed.add_field(name=f"<:settings:912336805808967733> Role Creation", value=f"`{role}`", inline=False)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(server(client))