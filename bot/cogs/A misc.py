import discord, random, math, asyncio
import giphy_client

from aiohttp import request
from modules import bot as v
from discord.ext import commands
from ._selectmenu import DropdownView


class invite(discord.ui.View):
	def __init__(self):
		super().__init__()

		self.add_item(discord.ui.Button(label='Invite', url="")) #bot invite link

class misc(commands.Cog):
    def __init__(self, client):
	    self.client = client

	#b!afk
	#b!rank
		
    @commands.command()
    async def help(self, ctx):
        em= discord.Embed(
		    color=v.hhelp,
		    title="BobCat Help Menu", 
		    description="""
			Bobcat is an simple to use bot. It has functions such as moderation, administration, entertainment, fun and other useful features
			""")
        
        em.set_thumbnail(url=self.client.user.avatar.url)
        await ctx.send(embed=em, view=DropdownView())

    @commands.command()
    async def invite(self, ctx):
	    inv = discord.Embed(color=v.yellow)
	    inv.add_field(name="Invite Me", value=f"Click the button", inline=False)
	    await ctx.send(
		    embed=inv,
		    view=invite()
	    )
	
    @commands.command(aliases=["pong"])
    async def ping(self, ctx):
        ping_Embed = discord.Embed(color=v.yellow)
        ping_Embed.add_field(name="Bot's Latency", value=f"<:dot:909416483082346516> Ping: `{round(self.client.latency*1000)}ms`", inline=False)
        await ctx.send(embed=ping_Embed)

    @commands.command()
    async def dead(self, ctx):
        dead_Embed = discord.Embed(color=v.yellow, timestamp=ctx.message.created_at)
        dead_Embed.add_field(name="Dead Chat", value=f"The chat was declared dead by {ctx.author.display_name}", inline=False)
        await ctx.message.delete()
        await ctx.send(embed=dead_Embed)

    @commands.command()
    async def diceroll(self, ctx):
        num = ["1","2","3","4","5","6"]

        coin1 = discord.Embed(title="Rolling A Dice...", color=v.yellow)
        mes = await ctx.send(embed=coin1)

        coin2 = discord.Embed(title="Result...", description=f"{random.choice(num)}", color=v.yellow)
        await mes.edit(embed=coin2)

    @commands.command(aliases=["flip"])
    async def coinflip(self, ctx):
        coin = ["Heads", "Tales"]
        
        coin1 = discord.Embed(title="Fliping A Coin...", color=v.yellow)
        mes = await ctx.send(embed=coin1)
        
        coin2 = discord.Embed(title="Result...", description=f"{random.choice(coin)}", color=v.yellow)
        await mes.edit(embed=coin2)

    @commands.command(aliases=['8ball','ask'])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]

        em = discord.Embed(title='Magic 8ball!', description=f"Let me think...", colour=v.yellow)
        msg = await ctx.send(embed=em)
        
        em = discord.Embed(description=f"**Question:** {question} \n**Answer:** {random.choice(responses)}", colour=v.yellow)

        await asyncio.sleep(1)
        await msg.edit(embed=em)

    @commands.command(aliases=["suggestion"])
    async def suggest(self, ctx, trigger, *, suggestion: str):
        em = discord.Embed(title="Your suggestion has been recorded!", color=v.green, timestamp=ctx.message.created_at)
        await ctx.reply(embed=em)

        sugg_em = discord.Embed(title=f"New Suggestion", color=v.yellow, timestamp=ctx.message.created_at)
        sugg_em.set_thumbnail(url=ctx.author.avatar.url)
        sugg_em.add_field(name=f"**Trigger:**", value=f"{trigger}", inline=False)
        sugg_em.add_field(name=f"**Response:**", value=f"{suggestion}", inline=False)
        sugg_em.add_field(name=f"**Suggested by:**", value=f"{ctx.author.display_name}", inline=False)
        mes = self.client.get_channel(0000000) # id of channel
        await mes.send(embed=sugg_em)
    @suggest.error
    async def suggest_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            error=discord.Embed(title="Missing Required Argument please do \n!suggest {trigger} {suggestion}", color=0xed5757, timestamp=ctx.message.created_at)
            await ctx.send(embed=error)
            return

    @commands.command()
    async def hug(self, ctx, member: discord.Member=None):
        api_instance = giphy_client.DefaultApi()
        api_responce = api_instance.gifs_search_get("8DNf3lniL8mCyoqKg4HQHP6Hhv0oqM4q", "anime hug" , limit=5, rating="g")
        lst = list(api_responce.data)
        giff = random.choice(lst)

        if member == None:
            hugs = discord.Embed(description="Mention a member that you want to hug", color=v.error)
            await ctx.send(embed=hugs)
            return

        if member == ctx.message.author:
            hug = discord.Embed(color=v.yellow)
            hug.set_author(name=f"You can't hug yourself, but i can hug you")
            await ctx.send(embed=hug)
            return

        else:
            embed=discord.Embed(color=v.yellow, timestamp=ctx.message.created_at)
            embed.add_field(name="Hugs", value=f"{ctx.author.mention} hugged {member.mention}")
            embed.set_image(url=f"https://media.giphy.com/media/{giff.id}/giphy.gif")
            await ctx.send(embed=embed)

    @commands.command(aliases=["hotcalc", "hot"])
    async def howhot(self, ctx, *, user: discord.Member = None):
        user = user or ctx.author
        userid = int(user.id)

        float((abs(math.sin(userid))) * 100)
        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        if hot > 25:
            emoji = "❤"
        elif hot > 50:
            emoji = "💖"
        elif hot > 75:
            emoji = "💞"
        else:
            emoji = "💔"

        embed = discord.Embed(title=f"{user.name} Your Love Percentage", colour=v.yellow)
        embed.add_field(name="Your love %", value=f"{hot:.2f}% {emoji}")
        mess = await ctx.send(embed=embed)
        await mess.add_reaction(emoji)

    @commands.command()
    async def lovecalc(self, ctx, user1: discord.Member, user2: discord.Member):
        user = user1 and user2
        userid = int(user.id)

        float((abs(math.sin(userid))) * 100)
        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        if hot > 25:
            emoji = "❤"
        elif hot > 50:
            emoji = "💖"
        elif hot > 75:
            emoji = "💞"
        else:
            emoji = "💔"

        embed = discord.Embed(title=f"Love between {user1.name} & {user2.name}", colour=v.yellow)
        embed.add_field(name="Love calculated", value=f"{emoji} {hot:.2f}% {emoji}", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def insult(self, ctx, user: discord.Member=None):
        user = user or ctx.author

        URl = f"https://evilinsult.com/generate_insult.php?lang=en&type=json"
        async with request("GET", URl) as res:
            if res.status == 200:
                evil_insult = await res.json()
                em = discord.Embed(title=f"New Instult for {user.display_name}")
                em.add_field(name=f"Hey, {ctx.author.name} please bear in mind these can be a bit harsh", value=f"** **", inline=False)
                em.add_field(name=f"{user.name} your insult is", value=f"||{evil_insult['insult']}|| (Click the blck bar to reveal)")
                await ctx.send(embed=em)

def setup(client):
	client.add_cog(misc(client))