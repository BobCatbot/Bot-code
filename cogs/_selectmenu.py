import discord
from discord.ext import commands
from modules import bot as v

class Button(discord.ui.View):
    @discord.ui.button(label='Go Back', style=discord.ButtonStyle.red)
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        em= discord.Embed(
            color=v.hhelp,
            title="BobCat Help Menu", 
            description="""
            Bobcat is a simple to use bot. It has functions such as moderation, administration, entertainment, and many more.
            """)

        em.set_thumbnail(url=v.banner)

        await interaction.response.edit_message(embed=em, view=DropdownView())
        

class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="General", description="General Commands", emoji="🔵"
            ),
            discord.SelectOption(
                label="Moderation", description="Moderation Commands", emoji="🔵"
                ),
            discord.SelectOption(
                label="Money", description="Money Commands", emoji="🔵"
            ),
            discord.SelectOption(
                label="Utils", description="User and Server Commands", emoji="🔵"
            ),
            discord.SelectOption(
                label="Animal", description="Animal Command", emoji="🔵"
            ),
        ]
        super().__init__(
            placeholder="Make a selcetion",
            min_values=1,
            max_values=1,
            options=options,
            disabled=False
        )

    async def callback(self, interaction: discord.Interaction):
        pre = v.bot.get_value(interaction.guild.id, "prefix")

        if self.values[0] == "General":
            em1 = discord.Embed(color=v.hhelp, description=f"""
            {pre.data}rank | [Usage](https://www.docs.bobcatbot.xyz/general/rank)
            {pre.data}afk | [Usage](https://www.docs.bobcatbot.xyz/general/afk)
            {pre.data}invite | [Usage](https://www.docs.bobcatbot.xyz/general/invite)
            {pre.data}ping | [Usage](https://www.docs.bobcatbot.xyz/general/ping)
            {pre.data}dead | [Usage](https://www.docs.bobcatbot.xyz/general/dead)
            {pre.data}diceroll | [Usage](https://www.docs.bobcatbot.xyz/general/diceroll)
            {pre.data}coinflip | [Usage](https://www.docs.bobcatbot.xyz/general/coinflip)
            {pre.data}8ball | [Usage](https://www.docs.bobcatbot.xyz/general/8ball)
            {pre.data}suggest | [Usage](https://www.docs.bobcatbot.xyz/general/suggestion)
            {pre.data}hug | [Usage](https://www.docs.bobcatbot.xyz/general/hug)
            {pre.data}howhot | [Usage](https://www.docs.bobcatbot.xyz/general/howhot)
            {pre.data}lovecalc | [Usage](https://www.docs.bobcatbot.xyz/general/lovecalc)
            {pre.data}insult | [Usage](https://www.docs.bobcatbot.xyz/general/insult)
            """)

            em1.set_author(icon_url=v.banner, name="General Commands.")
            em1.set_thumbnail(url=v.banner)
            await interaction.response.edit_message(embed=em1, view=Button())
        
        if self.values[0] == "Moderation":
            em = discord.Embed(color=v.hhelp, description=f"""
            {pre.data}clear | [Usage](https://www.docs.bobcatbot.xyz/moderation/clear)
            {pre.data}kick | [Usage](https://www.docs.bobcatbot.xyz/moderation/kick)
            {pre.data}ban | [Usage](https://www.docs.bobcatbot.xyz/moderation/ban)
            {pre.data}unban | [Usage](https://www.docs.bobcatbot.xyz/moderation/unban)
            {pre.data}mute | [Usage](https://www.docs.bobcatbot.xyz/moderation/mute)
            {pre.data}unmute | [Usage](https://www.docs.bobcatbot.xyz/moderation/unmute)
            {pre.data}slowmode | [Usage](https://www.docs.bobcatbot.xyz/moderation/slowmode)
            {pre.data}poll | [Usage](https://www.docs.bobcatbot.xyz/moderation/poll)
            {pre.data}giveaway | [Usage](https://www.docs.bobcatbot.xyz/moderation/giveaway)
            {pre.data}steal | [Usage](https://www.docs.bobcatbot.xyz/moderation/emoji)
            {pre.data}lockdown | [Usage](https://www.docs.bobcatbot.xyz/moderation/lockdown)
            {pre.data}unlock | [Usage](https://www.docs.bobcatbot.xyz/moderation/)
            """)

            em.set_author(icon_url=v.banner, name="Moderation commands.")

            await interaction.response.edit_message(embed=em, view=Button())

        if self.values[0] == "Money":
            em = discord.Embed(color=v.hhelp, description=f"""
            {pre.data}leaderboard | [Usage](https://www.docs.bobcatbot.xyz/money/leaderboard)
            {pre.data}shop | [Usage](https://www.docs.bobcatbot.xyz/money/shop)
            {pre.data}balance | [Usage](https://www.docs.bobcatbot.xyz/money/balance)
            {pre.data}work | [Usage](https://www.docs.bobcatbot.xyz/money/work)
            {pre.data}withdraw | [Usage](https://www.docs.bobcatbot.xyz/money/withdraw)
            {pre.data}deposit | [Usage](https://www.docs.bobcatbot.xyz/money/deposit)
            {pre.data}send | [Usage](https://www.docs.bobcatbot.xyz/money/send)
            {pre.data}rob | [Usage](https://www.docs.bobcatbot.xyz/money/rob)
            {pre.data}buy | [Usage](https://www.docs.bobcatbot.xyz/money/buy)
            {pre.data}sell | [Usage](https://www.docs.bobcatbot.xyz/money/sell)
            """)
            em.set_author(icon_url=v.banner, name="Money commands.")

            await interaction.response.edit_message(embed=em, view=Button())

        if self.values[0] == "Utils":
            em = discord.Embed(color=v.hhelp, description=f"""
            __**Utils Commands**__
            {pre.data}avatar | [Usage](https://www.docs.bobcatbot.xyz/user/avatar)
            {pre.data}userinfo | [Usage](https://www.docs.bobcatbot.xyz/user/userinfo)
            
            __**Server Commands**__
            {pre.data}membercount | [Usage](https://www.docs.bobcatbot.xyz/server/membercount)
            {pre.data}servericon | [Usage](https://www.docs.bobcatbot.xyz/server/servericon)
            {pre.data}serverbanner | [Usage](https://www.docs.bobcatbot.xyz/server/serverbanner)
            {pre.data}serverinfo | [Usage](https://www.docs.bobcatbot.xyz/server/serverinfo)
            {pre.data}roleinfo | [Usage](https://www.docs.bobcatbot.xyz/server/roleinfo)
            """)

            em.set_author(icon_url=v.banner, name="Utils commands.")

            await interaction.response.edit_message(embed=em, view=Button())
            
        if self.values[0] == "Animal":
            em = discord.Embed(color=v.hhelp, description=f"""
            {pre.data}cat | [Usage](https://www.docs.bobcatbot.xyz/animal/cat) 
            {pre.data}dog | [Usage](https://www.docs.bobcatbot.xyz/animal/dog)
            {pre.data}fox | [Usage](https://www.docs.bobcatbot.xyz/animal/fox)
            {pre.data}panda | [Usage](https://www.docs.bobcatbot.xyz/animal/panda)
            {pre.data}bird | [Usage](https://www.docs.bobcatbot.xyz/animal/bird)
            {pre.data}koala | [Usage](https://www.docs.bobcatbot.xyz/animal/koala)
            """)

            em.set_author(icon_url=v.banner, name="Animal commands.")

            await interaction.response.edit_message(embed=em, view=Button())

class DropdownView(discord.ui.View):
	def __init__(self):
		super().__init__()
		
		self.add_item(Dropdown())

class menu(commands.Cog):
	def __init__(self, client):
		self.client = client

def setup(client):
    client.add_cog(menu(client))