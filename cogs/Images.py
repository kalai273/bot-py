
import discord
from discord.ext import commands
import random
import requests
import asyncio
import aiohttp
import discord
import requests
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks

class Gif(commands.Cog, name="gif"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="kiss",
        description="kiss your friend.",
     ) 
    @checks.not_blacklisted()
    async def kiss(self, ctx: Context, member: discord.User) -> None:
      search_term = "anime kiss"
      apikey = "DZ2JR8TMALJU"
      lmt = 50

      r = requests.get(
            f"https://g.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

      gif_list = []
      sadReplyList = [
            f"Aw come on {ctx.author.name}, I'll give you a kiss \U0001f97a", f"That's sad, {ctx.author.name} :("]

      if r.status_code != 200:
            raise CustomException("Error connecting to the Tenor API")

      data = r.json()
      for details in data["results"]:
            gif_list.extend(media["gif"]["url"] for media in details["media"])
      if member == ctx.author:
            await ctx.send(random.choice(sadReplyList))
      else:
            embed = discord.Embed()
            embed.title = f"{ctx.author.name} kisses {member.name}"
            embed.set_image(url=random.choice(gif_list))
            await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="slap",
        description="slap your friend.",
     ) 
    @checks.not_blacklisted()
    async def slap(self, ctx: Context, member: discord.User) -> None:
        search_term = "anime slap"
        apikey = "DZ2JR8TMALJU"
        lmt = 50

        r = requests.get(
            f"https://g.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

        gif_list = []
        sadReplyList = [
            f"Chill {ctx.author.name}, Don't hurt yourself >:(", f"{ctx.author.name} why :("]

        if r.status_code != 200:
            raise CustomException("Error connecting to the Tenor API")

        data = r.json()
        for details in data["results"]:
            gif_list.extend(media["gif"]["url"] for media in details["media"])
        if member == ctx.author:
            await ctx.send(random.choice(sadReplyList))
        else:
            embed = discord.Embed(
              color=0xDA004E
            )
            embed.title = f"{ctx.author.name} slaps {member.name}"
            embed.set_image(url=random.choice(gif_list))
            await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="punch",
        description="punch your friend.",
         ) 
    @checks.not_blacklisted()
    async def punch(self, ctx: Context, member: discord.User) -> None:
        search_term = "anime punch"
        apikey = "DZ2JR8TMALJU"
        lmt = 50

        r = requests.get(
            f"https://g.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

        gif_list = []
        sadReplyList = [
            f"Tf are you doing {ctx.author.name}? Don't! \U0001f624", f"{ctx.author.name} DON'T PUNCH YOURSELF"]

        if r.status_code != 200:
            raise CustomException(
            "Error connecting to the Tenor API"
            )

        data = r.json()
        for details in data["results"]:
            gif_list.extend(media["gif"]["url"] for media in details["media"])

        if member == ctx.author:
          await ctx.send(random.choice(sadReplyList))
    
        else:

           embed = discord.Embed(color=0xDA004E)
           embed.title = f"{ctx.author.name} punches {member.name}"
           embed.set_image(
            url=random.choice(gif_list)
          )
           
        await ctx.send(embed=embed)
            
            
    @commands.hybrid_command(
        name="hug",
        description="hug your friend.",
         ) 
    @checks.not_blacklisted()
    async def hug(self, ctx: Context, member: discord.User) -> None:
        search_term = "anime hug"
        apikey = "DZ2JR8TMALJU"
        lmt = 50

        r = requests.get(
            f"https://g.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

        gif_list = []
        sadReplyList = [
            f"Do you want a hug {ctx.author.name}? \U0001f97a", f"Aw {ctx.author.name} :("]

        if r.status_code != 200:
            raise CustomException("Error connecting to the Tenor API")

        data = r.json()
        for details in data["results"]:
            gif_list.extend(media["gif"]["url"] for media in details["media"])
        if member == ctx.author:
            await ctx.send(random.choice(sadReplyList))
        else:
            embed = discord.Embed(
              color=0xDA004E
            )
            embed.title = f"{ctx.author.name} hugs {member.name}"
            embed.set_image(url=random.choice(gif_list))
            await ctx.send(embed=embed)
 
    @commands.hybrid_command(
        name="cuddle",
        description="cuddle your friend.",
         ) 
    @checks.not_blacklisted()
    async def cuddle(self, ctx: Context, member: discord.User) -> None:
        search_term = "anime cuddle"
        apikey = "DZ2JR8TMALJU"
        lmt = 50

        r = requests.get(
            f"https://g.tenor.com/v1/search?q={search_term}&key={apikey}&limit={lmt}")

        gif_list = []
        sadReplyList = [
            f"I'm here for you {ctx.author.name} \U0001f97a", f"Aw {ctx.author.name} :("]

        if r.status_code != 200:
            raise CustomException("Error connecting to the Tenor API")

        data = r.json()
        for details in data["results"]:
            gif_list.extend(media["gif"]["url"] for media in details["media"])
        if member == ctx.author:
            await ctx.send(random.choice(sadReplyList))
        else:
            embed = discord.Embed(
              color=0xDA004E
            )
            embed.title = f"{ctx.author.name} cuddles {member.name}"
            embed.set_image(url=random.choice(gif_list))
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Gif(bot))
