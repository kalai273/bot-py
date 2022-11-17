import asyncio 
from random import randint
import aiohttp
import discord
import requests
import wikipedia
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown



class Calculator(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.description="<:sucess:935052640449077248> Calculator "

    @commands.hybrid_command(
      name="calculate",
      aliases=["calc"], 
      description="Calculates the given expression")
    async def calc(self, ctx, *, expression):
        if len(expression) > 10000:
            await ctx.send("**I dont think I can bear that much**")
        else:
            st = expression.replace("+", "%2B")
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://api.mathjs.org/v4/?expr={st}"
                ) as response:
                    ex = await response.text()
                    if len(ex) > 20000:
                        await ctx.send("I dont think I can bear that much")
                    else:

                        embed = discord.Embed(
                            timestamp=ctx.message.created_at,
                            description="Here is the result ",
                            color=0xDA004E
                        )
                        embed.add_field(
                            name=f"Expression", value=f"```css\n{expression}```", inline=False
                        )                      
                        embed.add_field(
                            name=f"Result", value=f"```css\n{ex}```", inline=False
                        )
                        
                        embed.set_author(
                            name="Calculator"
                            
                        )
                        embed.set_thumbnail(url="https://www.involve.me/assets/images/blog/how-to-create-a-simple-price-calculator-and-capture-more-leads/calculator-L.png",)
                        await ctx.send(embed=embed)


    @commands.hybrid_command(
        cooldown_after_parsing=True, description="Shows wikipedia summary"
    )
    @cooldown(1, 10, BucketType.user)
    async def wiki(self, ctx, *, msg):
        try:
            content = wikipedia.summary(msg, auto_suggest=False, redirect=True)

            embed = discord.Embed(title="Wikipedia", color=0xDA004E)
            chunks = [content[i : i + 1024] for i in range(0, len(content), 2000)]
            for chunk in chunks:
                embed.add_field(name="\u200b", value=chunk, inline=False)
            await ctx.send(embed=embed)
        except:
            await ctx.send(embed = discord.Embed(title="**Failed to get information**",description='No results for that topic, kindly search again and be sure to check case and spelling !',color=0xDA004E))

    @commands.hybrid_command(
        cooldown_after_parsing=True,
        description="Search the wikipedia and see the results",
    )
    @cooldown(1, 5, BucketType.user)
    async def search_wiki(self, ctx, *, msg):
        try:

            content = wikipedia.search(msg, results=5, suggestion=True)
            content = content[0]
            embed = discord.Embed(title="Search Results", color=0xDA004E)
            z = 1
            for i in content:
                embed.add_field(name="\u200b", value=f"{z}-{i}", inline=False)
                z += 1

            await ctx.send(embed=embed)
        except:
            await ctx.send("**Failed to get information**")


async def setup(client):
    await client.add_cog(Calculator(client))