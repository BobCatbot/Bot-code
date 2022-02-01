import discord, datetime, random, asyncio, aiohttp
from io import BytesIO
from discord.ext import commands
from modules import bot as v

class mod(commands.Cog):
    def __init__(self, client):
        self.client = client

	#clear, kick, ban, unban, mute, unmute, slowmode, poll, giveaway, createemoji, lockdown, unlock

	# clear [amount]
    @commands.command(aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=0):
        if amount == 0:
            clear = discord.Embed(title="❌ The amount cant be 0!", color=v.error)
            await ctx.send(embed=clear)
            return

        if amount < 0:
            clear = discord.Embed(title="❌ The amount must be positive!", color=v.error)
            await ctx.send(embed=clear)
            return

        if amount > 150:
            clear = discord.Embed(title="❌ You cannot delete more then 150 messages!", color=v.error)
            await ctx.send(embed=clear)
            return

        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Cleared {amount} messages", delete_after=5.0)
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            error=discord.Embed(title="❌ Missing `Manage Messages` permission", color=v.error)
            await ctx.send(embed=error)
            return

    # kick [member] [reason]
    @commands.command(aliases=["k"])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member=None, *, reason=None):
        if member == ctx.guild.owner:
            kick = discord.Embed(title="❌ You can't kick the owner of this server", color=v.error)
            await ctx.send(embed=kick)
            return

        if member == ctx.message.author:
            kick = discord.Embed(title="❌ You can't kick yourself", color=v.error)
            await ctx.send(embed=kick)
            return

        if member == None:
            kick = discord.Embed(title="❌ Mention the member you want to kick", color=v.error)
            await ctx.send(embed=kick)
            return

        if member.top_role >= ctx.author.top_role:
            kick = discord.Embed(title="❌ You can only moderate members below your role", color=v.error)
            await ctx.send(embed=kick)    
            return

        else:
            await member.kick(reason=reason)

            embed = discord.Embed()
            embed.set_author(name=f"{member} has been kicked", icon_url=member.avatar.url)
            embed.add_field(name=f"Reason: {reason}", value="** **")
            await ctx.send(embed=embed)
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            error=discord.Embed(title="❌ Missing `kick Members` permission", color=v.error)
            await ctx.send(embed=error)
            return

# ban [member] [reason]
    @commands.command(aliases=["b"])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member=None, *, reason=None):
        if member == ctx.guild.owner:
            ban = discord.Embed(title="❌ You can't ban the owner of this server", color=v.error)
            await ctx.send(embed=ban)
            return

        if member == ctx.message.author:
            ban = discord.Embed(title="❌ You can't ban yourself", color=v.error)
            await ctx.send(embed=ban)
            return

        if member == None:
            ban = discord.Embed(title="❌ Mention a member that you want to ban", color=v.error)
            await ctx.send(embed=ban)
            return

        if member.top_role >= ctx.author.top_role:
            kick = discord.Embed(title="❌ You can only moderate members below your role", color=v.error)
            await ctx.send(embed=kick)    
            return

        else:
            await member.ban(reason=reason)

            embed = discord.Embed()
            embed.set_author(name=f"{member} has been banned", icon_url=member.avatar.url)
            embed.add_field(name=f"Reason: {reason}", value="** **")
            await ctx.send(embed=embed)
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            error=discord.Embed(title="❌ Missing `Ban Members` permission", color=v.error)
            await ctx.send(embed=error)
            return

# unban [member]
    @commands.command(aliases=["ub"])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.User=None):
        if member == None:
            ban = discord.Embed(title="❌ Mention a member that you want to ban", color=v.error)
            await ctx.send(embed=ban)
            return

        if member.top_role >= ctx.author.top_role:
            kick = discord.Embed(title="❌ You can only moderate members below your role", color=v.error)
            await ctx.send(embed=kick)    
            return

        else:
            await ctx.guild.unban(user=member)

            embed = discord.Embed()
            embed.set_author(name=f"{member} has been unbanned", icon_url=member.avatar.url)
            await ctx.send(embed=embed)
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            error=discord.Embed(title="❌ Missing `Ban Members` permission", color=v.error)
            await ctx.send(embed=error)
            return
        
# mute
    @commands.command(aliases=["m"])
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member=None, *, reason=None):
        if member == ctx.guild.owner:
            mute = discord.Embed(title="❌ You can't mute the owner of this server", color=v.error)
            await ctx.send(embed=mute)
            return

        if member == ctx.message.author:
            mute = discord.Embed(title="❌ You can't mute yourself", color=v.error)
            await ctx.send(embed=mute)
            return

        if member == None:
            mute = discord.Embed(title="❌ Mention a member you want to mute", color=v.error)
            await ctx.send(embed=mute)
            return

        if member.top_role >= ctx.author.top_role:
            kick = discord.Embed(title="❌ You can only moderate members below your role", color=v.error)
            await ctx.send(embed=kick)    
            return
        
        else:
            mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

            for channel in ctx.guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False)
            
            await member.add_roles(mutedRole, reason=reason)
            
            embed = discord.Embed()
            embed.set_author(name=f"{member} has been muted", icon_url=member.avatar.url)
            embed.add_field(name=f"Reason: {reason}", value="** **")
            await ctx.send(embed=embed)
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            error=discord.Embed(title="❌ Missing `kick Members` permission", color=v.error)
            await ctx.send(embed=error)
            return

# unmute
    @commands.command(aliases=["um"])
    @commands.has_permissions(kick_members=True)   
    async def unmute(self, ctx, member: discord.Member=None):
        if member == None:
            unmute = discord.Embed(title="❌ Mention a member you want to unmute", color=v.error)
            await ctx.send(embed=unmute)
            return

        if member.top_role >= ctx.author.top_role:
            kick = discord.Embed(title="❌ You can only moderate members below your role", color=v.error)
            await ctx.send(embed=kick)    
            return

        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mutedRole in [role.id for role in member.roles]:
            await ctx.send("Memeber isnt muted dummy")
            return
            
        else:
            mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
            await member.remove_roles(mutedRole)
            
            embed = discord.Embed()
            embed.set_author(name=f"{member} has been unmuted", icon_url=member.avatar.url)
            await ctx.send(embed=embed)
    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            error=discord.Embed(title="❌ Missing `kick Members` permission", color=v.error)
            await ctx.send(embed=error)
            return

    @commands.command(aliases=["sm"])
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        if seconds == None:
            mute = discord.Embed(title="❌ You forgot to put an amount of seconds!", color=v.error)
            await ctx.send(embed=mute)
            return 

        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"{ctx.channel.mention} is now in slowmode of {seconds} seconds :)")

    @slowmode.error
    async def slowmode_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            error=discord.Embed(title="❌ Missing `Manage Channels` permission", color=v.error)
            await ctx.send(embed=error)
            return

# poll [message]
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def poll(self, ctx, *, message):
        embed = discord.Embed(
            title="Poll",
            description=f'{message}'
        )
            
        await ctx.message.delete()
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            error=discord.Embed(title="❌ Missing `Manage Messages` permission", color=v.error)
            await ctx.send(embed=error)
            return

#giveaway [mins] [prize]
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def giveaway(self, ctx, mins : int, * , prize: str):
        embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = v.yellow)

        end = datetime.datetime.utcnow() + datetime.timedelta(seconds = mins*60) 

        content = ":tada: **GIVEAWAY ** :tada:"
        embed = discord.Embed(
            title=f"**{prize}**",
            description=f'React with :tada: to enter! \n Ends: {end} UTC \nHosted by: {ctx.author.mention}')
        embed.set_footer(text = f"Ends {mins} mintues from now!")
        my_msg = await ctx.send(content=content, embed=embed)

        await my_msg.add_reaction("🎉")
        await asyncio.sleep(mins*60)

        new_msg = await ctx.channel.fetch_message(my_msg.id)
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))
        winner = random.choice(users)
        await ctx.send(f"Congratulations! {winner.mention} won `{prize}`!")

        content = ":tada: **GIVEAWAY ENDED** :tada:"
        embed = discord.Embed(
            title=f"{prize}",
            description=f'Winner: {winner.mention} \nHosted By: {ctx.author.mention}')
        embed.set_footer(text = f"Ended • ")

        await my_msg.edit(content=content, embed=embed)
    @giveaway.error
    async def giveaway_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            error=discord.Embed(title="❌ Missing `Manage Channels` permission", color=v.error)
            await ctx.send(embed=error)
            return

# stealemoji [url] [name]
    @commands.command(aliases=["addemoji", "ae", "ce", "steal"])
    @commands.has_permissions(manage_emojis=True)
    async def createemoji(self, ctx, url: str, *, name):
        guild = ctx.guild
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url) as r:
                try:
                    img_or_gif = BytesIO(await r.read())
                    b_value = img_or_gif.getvalue()
                    if r.status in range(200, 299):
                        emojis = await guild.create_custom_emoji(image=b_value, name=name)
                        await ctx.message.delete()
                        await ctx.send(f"Successfully created emoji: <:{name}:{emojis.id}>")
                        await ses.close()
                        
                    else:
                        await ctx.send(f'❌ Error when making request | {r.status} response.')
                        await ses.close()
                        
                except discord.HTTPException:
                    await ctx.send('❌ File size is too big!')
                
    @createemoji.error
    async def createemoji_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            error=discord.Embed(title="❌ Missing `Manage Emojis` permission", color=v.error)
            await ctx.send(embed=error)
            return

# lockdown
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx, channel: discord.TextChannel=None):
        if channel == None:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
            await ctx.send(ctx.channel.mention + " Is now in lockdown!")
            return

        else:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            await ctx.message.add_reaction("🔒")
            await channel.send("This channel is now on `lockdown`")
    @lockdown.error
    async def lockdown_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            error=discord.Embed(title="❌ Missing `Manage Channels` permission", color=v.error)
            await ctx.send(embed=error)
            return

# unlock
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel=None):
        if channel == None:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
            await ctx.send(ctx.channel.mention + " Has been unlocked!")
            return
        
        else:
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
            await ctx.message.add_reaction("🔓")
            await channel.send("This channel is now `unlocked`")
    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            error=discord.Embed(title="❌ Missing `Manage Channels` permission", color=v.error)
            await ctx.send(embed=error)
            return
        
    @commands.command(aliases=["giverole"])
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, user : discord.Member=None, *, role : discord.Role=None):
        if user == None:
            error = discord.Embed(description="Invalid usage! `giverole @member @role`", color=v.error)
            await ctx.send(embed=error)
            
        if role.position > ctx.author.top_role.position:
            error=discord.Embed(title="❌ That role is above your top role", color=v.error)
            await ctx.send(embed=error)
            return 

        if role in user.roles:
            error=discord.Embed(title="❌ You already have this role", color=v.error)
            await ctx.send(embed=error)

        else:
            await user.add_roles(role)

            role = discord.Embed(description=f"Role {role.mention} was added to {user.mention}", color=v.yellow)
            await ctx.send(embed=role)

    @addrole.error
    async def addrole_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            error=discord.Embed(title="❌ Missing `Manage Roles` permission.", color=v.error)
            await ctx.send(embed=error)
            return

    @commands.command(aliases=["takerole"])
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, user : discord.Member=None, role : discord.Role=None):
        if user == None:
            error = discord.Embed(description="Invalid usage! `giverole @member @role`", color=v.error)
            await ctx.send(embed=error)
            
        if role.position > ctx.author.top_role.position:
            error=discord.Embed(title="❌ That role is above your top role", color=v.error)
            await ctx.send(embed=error)
            return 

        if role in user.roles:
            await user.remove_roles(role)
            role = discord.Embed(description=f"Removed {role.mention} from {user.mention}", color=v.yellow)
            await ctx.send(embed=role)
    @removerole.error
    async def removerole_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            error=discord.Embed(title="❌ Missing `Manage Roles` permission.", color=v.error)
            await ctx.send(embed=error)            

def setup(client):
    client.add_cog(mod(client))