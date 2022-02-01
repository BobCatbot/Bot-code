import discord
from discord.ext import commands
from modules import bot as v

class user(commands.Cog):
    def __init__(self, client):
        self.client = client

    #avatar, #userinfo, #me
    
    @commands.command()
    async def avatar(self, ctx, *,  member : discord.Member=None):
        if member is None:
            member = ctx.author

        embed = discord.Embed(title=f"{member.display_name}'s Avatar!", colour=v.yellow, timestamp=ctx.message.created_at)
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=["user-info", "u-info","uinfo"])
    async def userinfo(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        perm_list = [perm[0] for perm in member.guild_permissions if perm[1]]
        joined = member.joined_at.strftime("%a, %#d %B %Y")

        roles = [role for role in member.roles]
        roles = [role.mention for role in roles]

        userinfo_embed = discord.Embed(colour=member.colour, timestamp=ctx.message.created_at)
        userinfo_embed.set_author(name=f"user info - {member}")
        userinfo_embed.set_thumbnail(url=member.avatar.url)

        userinfo_embed.add_field(name="<:profile:912327649538474006> Name#Tag", value=f"`{member}`", inline=False)
        userinfo_embed.add_field(name="<:ID:912319260875960360> ID", value=f"`{member.id}`", inline=False)
        userinfo_embed.add_field(name="<:flag:912327154296061992> Top role", value=f"{member.top_role.mention}", inline=False)
        userinfo_embed.add_field(name="<:bluedot:911663595035713596> Permissions", value=f"`{perm_list}`", inline=False)
        userinfo_embed.add_field(name=f"<:moderation:912319464572334140> Roles ({len(roles)})", value=f"{roles}", inline=False)        
        userinfo_embed.add_field(name="<:boosts:912319595048763402> Booster", value=f"`{(str(bool(member.premium_since)))}`", inline=False)
        userinfo_embed.add_field(name="<:join:912328324796264468> Joined at", value=f"`{joined}`", inline=False)

        userinfo_embed.set_footer(text=f" |   {ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=userinfo_embed)

    @commands.command()
    async def me(self, ctx):
        member = ctx.author

        me = discord.Embed(color=v.yellow)
        me.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar.url)
        me.add_field(name=f"Info on {member.name}", value=f"{member.mention} | `{member.display_name}` | `{member}` | `{member.id}`")
        await ctx.send(embed=me)


def setup(client):
    client.add_cog(user(client))