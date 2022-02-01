# packages that are needed
import discord
import json

from discord.ext import commands
from modules import bot as v

class AFK(commands.Cog):
	def __init__(self, client):
			self.client = client

	@commands.Cog.listener()
	async def on_member_join(self, member):
		with open("databases/afk.json", "r") as f:
			afk = json.load(f)

		await update_data(afk, member)

		with open("databases/afk.json", "w") as f:
			json.dump(afk, f)

	@commands.Cog.listener()
	async def on_message(self, message):
		with open("databases/afk.json", "r") as f:
			afk = json.load(f)
		
		if not message.author.bot:
			await update_data(afk, message.author)
		
		with open("databases/afk.json", "w") as f:
			json.dump(afk, f)

			#mention a member
		for x in message.mentions:
			try:
				if afk[f"{x.id}"]["AFK"] == "True":
					reason1 = afk[f"{x.id}"]["Reason"]

					afk_mention= discord.Embed(color=v.yellow, timestamp=message.created_at)
					afk_mention.set_thumbnail(url=x.avatar.url)
					afk_mention.add_field(name="AFK", value=f"{x.mention} is AFK \n**Reason:** {reason1}", inline=False)
					afk_mention.set_footer(icon_url=message.author.avatar.url, text=f" |   {message.author.name}")
					await message.channel.send(embed=afk_mention, delete_after=v.delete)

					return

			except KeyError:
				pass
                  
	@commands.command()
	@commands.cooldown(rate=2, per=120.0, type=commands.BucketType.user)
	async def afk(self, ctx, *, reason=None):
		with open("databases/afk.json", "r") as f:
			afk = json.load(f)
					
		if afk[f"{ctx.author.id}"]["AFK"] == "False": #Gone afk
			afk[f"{ctx.author.id}"]["AFK"] = "True"
			reason1 = afk[f"{ctx.author.id}"]["Reason"] = f"{reason}"
			with open("databases/afk.json", "w") as f:
					json.dump(afk, f)

			embed=discord.Embed(
					description=f"{ctx.author.mention} you're now AFK \n**Reason:** {reason1}",
					color=v.yellow, 
					timestamp=ctx.message.created_at
					)
			embed.set_footer(icon_url=ctx.author.avatar.url, text=f" |   {ctx.author.name}#{ctx.author.discriminator}")
			await ctx.message.add_reaction("<:Bobcat:896319577837957130>")
			await ctx.channel.send(embed=embed, delete_after=v.delete)

			await ctx.author.edit(nick=f"AFK | {ctx.author.display_name}")

		else: # not afk
			afk[f"{ctx.author.id}"]["AFK"] = "False"
			afk[f"{ctx.author.id}"]["Reason"] = "None"
			with open("databases/afk.json", "w") as f:
				json.dump(afk, f)

			embed=discord.Embed(
				description=f"Welcome back {ctx.author.mention}",
				color=v.yellow, 
				timestamp=ctx.message.created_at
			)
			embed.set_footer(icon_url=ctx.author.avatar.url, text=f" |   {ctx.author.name}#{ctx.author.discriminator}")
			await ctx.message.add_reaction("<:Bobcat:896319577837957130>")
			await ctx.channel.send(embed=embed, delete_after=v.delete)

			await ctx.author.edit(nick=f"{ctx.author.display_name[6:]}")
		
		with open("databases/afk.json", "w") as f:
			json.dump(afk, f)

async def update_data(afk, user):
    if not f"{user.id}" in afk:
        afk[f"{user.id}"] = {}
        afk[f"{user.id}"]["AFK"] = "False"
        afk[f"{user.id}"]["Reason"] = "None"

def setup(client):
    client.add_cog(AFK(client))