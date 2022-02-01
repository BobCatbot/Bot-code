import aiohttp 
import discord
import random

from aiohttp import request
from discord.ext import commands
from modules import bot as v

class animal(commands.Cog):
        def __init__(self, client):
            self.client = client
                
        @commands.command()
        async def cat(self, ctx):
            url = "https://some-random-api.ml/facts/cat"

            async with request("GET", url, headers={}) as response:
                fact = await response.json()

                async with aiohttp.ClientSession() as cs:
                    async with cs.get("https://aws.random.cat/meow") as r:
                            
                        data = await r.json()

                        embed = discord.Embed(color=v.yellow)
                        embed.set_image(url=data["file"])
                        embed.set_footer(text=fact["fact"])
                        await ctx.send(embed=embed)

        @commands.command()
        async def dog(self, ctx):
            url = "https://some-random-api.ml/facts/dog"

            async with request("GET", url, headers={}) as response:
                fact = await response.json()

            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://random.dog/woof.json") as r:
                        
                    data = await r.json()

                    embed = discord.Embed(color=v.yellow)
                    embed.set_image(url=data["url"])
                    embed.set_footer(text=fact['fact'])
                    await ctx.send(embed=embed)

        @commands.command()
        async def fox(self, ctx):
            url = "https://some-random-api.ml/facts/fox"

            async with request("GET", url, headers={}) as response:
                fact = await response.json()

            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://some-random-api.ml/img/fox") as r:
                    data = await r.json()

                    embed = discord.Embed(color=v.yellow)
                    embed.set_image(url=data["link"])
                    embed.set_footer(text=fact['fact'])
                    await ctx.send(embed=embed)

        @commands.command()
        async def panda(self, ctx):
            url = "https://some-random-api.ml/facts/panda"

            async with request("GET", url, headers={}) as response:
                fact = await response.json()

            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://some-random-api.ml/img/panda") as r:
                    data = await r.json()

                    embed = discord.Embed(color=v.yellow)
                    embed.set_image(url=data["link"])
                    embed.set_footer(text=fact['fact'])
                    await ctx.send(embed=embed)

        @commands.command()
        async def bird(self, ctx):
            url = "https://some-random-api.ml/facts/bird"

            async with request("GET", url, headers={}) as response:
                fact = await response.json()

            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://some-random-api.ml/img/birb") as r:
                        
                    data = await r.json()

                    embed = discord.Embed(color=v.yellow)
                    embed.set_image(url=data["link"])
                    embed.set_footer(text=fact['fact'])
                    await ctx.send(embed=embed)

        @commands.command()
        async def koala(self, ctx):
            url = "https://some-random-api.ml/facts/koala"

            async with request("GET", url, headers={}) as response:
                fact = await response.json()

            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://some-random-api.ml/img/koala") as r:
                        
                    data = await r.json()

                    embed = discord.Embed(color=v.yellow)
                    embed.set_image(url=data["link"])
                    embed.set_footer(text=fact['fact']) 
                    await ctx.send(embed=embed)

def setup(client):
    client.add_cog(animal(client))