import discord, json, random
from discord.ext import commands
from modules import bot as v

mainshop = [{"name":"Watch", "price":100, "description":"Time"},
            {"name":"Laptop", "price":1000, "description":"Work"},
            {"name":"PC", "price":10000, "description":"Gaming"},
            {"name":"Ferrari", "price":99999, "description":"Sports Car"}]

"""
Economy on/off: eco
Economy Emoji: emoji
Economy Name: iconame
"""
class money(commands.Cog):
    def __init__(self, client):
        self.client = client

    #leaderboard, balance, shop, work, withdraw, deposit, send, rob, buy, sell

    @commands.command(aliases = ["lb"])
    #@commands.cooldown(rate=1, per=120, type=commands.BucketType.user)
    async def leaderboard(self, ctx, x = 1):
        users = await get_bank_data()
        leader_board = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["wallet"] + users[user]["bank"]
            leader_board[total_amount] = name
            total.append(total_amount)

        total = sorted(total,reverse=True)    
        
        em = discord.Embed(
            title = f"Top {x} Richest People",
            description = "This is decided on the basis of raw money in the bank and wallet",
            color=0xffff00
            )

        index = 1
        for amt in total:
            id_ = leader_board[amt]
            member = self.client.get_user(id_)
            name = member.name
            
            em.add_field(name = f"{index}. {name} - {amt}" , value = f"** **",  inline = False)
            if index == x:
                break
            else:
                index += 1

        await ctx.send(embed = em)

    @commands.command()
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.user)
    async def shop(self, ctx):
        em = discord.Embed(title = f"Shop", color=0xffff00)

        for item in mainshop:
            name = item["name"]
            price = item["price"]
            em.add_field(name=name, value=f"`{price}`")

        await ctx.send(embed = em) 

    @commands.command(aliases=['bal'])
    @commands.cooldown(rate=2, per=20, type=commands.BucketType.user)
    async def balance(self, ctx, member: discord.Member=None):
        await open_account(ctx.author)
        users = await get_bank_data()
        
        try: 
            if member == None:
                users = await get_bank_data()
                wallet_amt = users[str(ctx.author.id)]["wallet"]
                bank_amt = users[str(ctx.author.id)]["bank"]

                em = discord.Embed(title=f'{ctx.author.name} Balance', color=0xffff00)
                em.add_field(name="Wallet Balance", value=wallet_amt, inline=True)
                em.add_field(name="Bank Balance", value=bank_amt, inline=True)

                await ctx.send(embed= em)
                return
            
            else:
                users = await get_bank_data()
                wallet_amt = users[str(member.id)]["wallet"]
                bank_amt = users[str(member.id)]["bank"]

                em = discord.Embed(title=f'{member.name} Balance', color=0xffff00)
                em.add_field(name="Wallet Balance", value=wallet_amt, inline=True)
                em.add_field(name="Bank Balance", value=bank_amt, inline=True)

                await ctx.send(embed= em)

        except ValueError:
            await ctx.send(f"{member.display_name} isnt in the database")


    @commands.command()
    @commands.cooldown(rate=1, per=3600, type=commands.BucketType.user)
    async def work(self, ctx):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        earnings = random.randrange(101)

        mes = f"{ctx.author.mention}"
        em = discord.Embed(
            description = f"{ctx.author.name} you started working again. You gain {earnings} from your last work. \nCome back in 1 hour",
            color=0xffff00
        )
        await ctx.send(content=mes, embed=em)

        users[str(user.id)]["wallet"] += earnings

        with open("databases/mainbank.json",'w') as f:
            json.dump(users,f)

    @commands.command(aliases=['wd'])
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.user)
    async def withdraw(self, ctx, amount = None):
         
        await open_account(ctx.author)
        if amount == None:
            await ctx.send("Please enter the amount")
            return
            
        bal = await update_bank(ctx.author)
        amount = int(amount)

        if amount > bal[1]:
            await ctx.send('You do not have sufficient balance')
            return

        if amount < 0:
            await ctx.send('Amount must be positive!')
            return

        await update_bank(ctx.author,amount)
        await update_bank(ctx.author,-1*amount,'bank')

        mes = f"{ctx.author.mention}"
        em = discord.Embed(
            title = f"You withdrew {amount}",
            color=0xffff00
        )
        await ctx.send(content=mes, embed=em)

    @commands.command(aliases=['dp'])
    @commands.cooldown(rate=1, per=100, type=commands.BucketType.user)
    async def deposit(self, ctx, amount = None):
        
        await open_account(ctx.author)
        if amount == None:
            await ctx.send(f"Please enter the amount")
            return

        bal = await update_bank(ctx.author)
        amount = int(amount)

        if amount > bal[0]:
            await ctx.send(f'You do not have sufficient balance')
            return

        if amount < 0:
            await ctx.send(f'Amount must be positive!')
            return

        await update_bank(ctx.author, -1*amount)
        await update_bank(ctx.author, amount, 'bank')
        
        mes = f"{ctx.author.mention}"
        em = discord.Embed(
            title = f"You deposited {amount}",
            color=0xffff00
        )
        await ctx.send(content=mes, embed=em)


    @commands.command()
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.user)
    async def send(self, ctx, member : discord.Member, amount = None):
        await open_account(ctx.author)
        await open_account(member)
        bal = await update_bank(ctx.author)

        if amount == None:
            await ctx.send(f"Please enter the amount")
            return

        if amount == 'all':
            amount = bal[0]

        amount = int(amount)

        if amount > bal[0]:
            await ctx.send(f'You do not have sufficient balance')
            return

        if amount < 0:
            await ctx.send(f'Amount must be positive!')
            return

        await update_bank(ctx.author, -1*amount, 'bank')
        await update_bank(member, amount, 'bank')

        if amount == "1":
            await ctx.send('tesr')
            return
        
        if amount > 2:
            em = discord.Embed(
                description = f"{ctx.author.mention} gave {member.mention} `{amount}`",
                color=0xffff00
            )
            await ctx.send(embed=em)

    @commands.command(aliases=['rb'])
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.user)
    async def rob(self, ctx, member : discord.Member):
        await open_account(ctx.author)
        await open_account(member)
        bal = await update_bank(member)
        
        if bal[0] < 100:
            await ctx.send(f'It is useless to rob him :(')
            return

        earning = random.randrange(0,bal[0])
        await update_bank(ctx.author,earning)
        await update_bank(member,-1*earning)

        mes = f"{ctx.author.mention}"
        em = discord.Embed(
            description = f"**You robbed {member.mention} and got {earning}**",
            color=0xffff00
        )
        await ctx.send(content=mes, embed=em)

    @commands.command()
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.user)
    async def buy(self, ctx, item, amount = 1):
        await open_account(ctx.author)
        res = await buy_this(ctx.author, item, amount)
        
        if not res[0]:
            if res[1] == 1:
                await ctx.send(f"That Object isn't there! {emoji or emojis.data}")
                return
            if res[1] == 2:
                await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
                return

        else:
            mes = f"{ctx.author.mention}"
            em = discord.Embed(
                description = f"You just bought `{amount}` `{item}`",
                color=0xffff00
            )
            await ctx.send(content=mes, embed=em)
    @buy.error
    async def buy_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
          pre = v.bot.get_value(ctx.guild.id, "prefix")
          await ctx.send(f"Your missing a item Please do {pre.data}shop to find them")
          return
        
    @commands.command()
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.user)
    async def sell(self, ctx,item,amount = 1):
          await open_account(ctx.author)
          res = await sell_this(ctx.author,item,amount)
          if not res[0]:
              if res[1]==1:
                  await ctx.send(f"That Object isn't there!")
                  return
              if res[1]==2:
                  await ctx.send(f"You don't have {amount} {item} in your bag.")
                  return
              if res[1]==3:
                  await ctx.send(f"You don't have {item} in your bag.")
                  return

          mes = f"{ctx.author.mention}"
          em = discord.Embed(
            description = f"You just sold `{amount}` `{item}`",
            color=0xffff00
          )
          await ctx.send(content=mes, embed=em)




async def open_account(user):
    with open ("databases/mainbank.json", "r") as f:
        users = json.load(f)
        
    if str(user.id) in users:
            return False
        
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open ("databases/mainbank.json", "w") as f:
        users = json.dump(users, f)
        
    return True

async def get_bank_data():
    with open('databases/mainbank.json','r') as f:
        users = json.load(f)
    return users

async def update_bank(user,change=0,mode = 'wallet'):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open('databases/mainbank.json','w') as f:
        json.dump(users,f)
    bal = users[str(user.id)]['wallet'],users[str(user.id)]['bank']
    return bal

    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0
    with open('databases/mainbank.json','w') as f:
        json.dump(users,f)
    return True




async def buy_this(user, item_name, amount):
    item_name = item_name
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break
    if name_ == None:
        return [False,1]
    cost = price*amount
    users = await get_bank_data()
    bal = await update_bank(user)
    if bal[0]<cost:
        return [False,2]
    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        
    with open("databases/mainbank.json","w") as f:
        json.dump(users,f)
    await update_bank(user,cost*-1,"wallet")
    return [True,"Worked"]

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.9* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("databases/mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]

def setup(client):
    client.add_cog(money(client))