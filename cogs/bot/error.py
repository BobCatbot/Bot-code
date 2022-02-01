import discord

from discord.ext import commands

class errors(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(color=discord.Color.red())
            em.add_field(name="Slow it down", value=f"Try again in `{error.retry_after:.0f}` seconds.\n The default cooldown is `{error.cooldown.rate}` per `{error.cooldown.per:.0f}` seconds")
            em.set_footer(icon_url=self.client.user.avatar.url, text=f'If you think this is a mistake please contact BananaBobs2004#2004 or Tech#0873')
            await ctx.send(embed=em)
            return
        
        if isinstance(error, commands.CommandNotFound):
            
            embed = discord.Embed(color=discord.Color.red())
            embed.add_field(name="Invalid Command!", value=f"Please type `b!help` to see all commands")
            embed.set_footer(icon_url=self.client.user.avatar.url, text=f'If you think this is a mistake please contact BananaBobs2004#2004 or Tech#0873')
            await ctx.send(embed=embed)
            return
        
        else:
            pass

def setup(client):
    client.add_cog(errors(client))