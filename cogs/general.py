import random
import time
import psutil
import json
import os
import requests
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context 
from helpers import checks


if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot
        self.config = config
        self.process = psutil.Process(os.getpid())

    @commands.hybrid_command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    @checks.not_blacklisted()
    async def about(self, ctx):
        """ About the bot """
        ramUsage = self.process.memory_full_info().rss / 1024**2
        avgmembers = sum(g.member_count for g in self.bot.guilds) / len(self.bot.guilds)

        embedColour = None
        if hasattr(ctx, "guild") and ctx.guild is not None:
            embedColour = 0xDAEDAF

        embed = discord.Embed(
          title=f"ℹ About **{ctx.bot.user}**",
          color=0xDA004E)
        embed.set_thumbnail(url=ctx.bot.user.avatar)
        
        embed.add_field(
            name=f"Developer{'' if len(self.config['owners']) == 1 else 's'}",
            value="\n".join([str(self.bot.get_user(x)) for x in self.config["owners"]])
        )
        embed.add_field(name="Library", value="**`discord.py`**")
        embed.add_field(name="Servers", value=f"**`{len(ctx.bot.guilds)} ( avg: {avgmembers:,.2f} users/server )`**")
        embed.add_field(name="Commands loaded", value=f"**`{len([x.name for x in self.bot.commands])}`**")
        embed.add_field(name="RAM", value=f"**`{ramUsage:.2f} MB`**")

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    @checks.not_blacklisted()
    async def serverinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the server.
        
        :param context: The hybrid command context.
        """
        roles = [role.name for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{context.guild}",
            color=0xDA004E
        )
        if context.guild.icon is not None:            
            embed.set_thumbnail(
                url=context.guild.icon.url
            )
        embed.add_field(
            name="Server ID",
            value=context.guild.id
        )
        embed.add_field(
            name="Member Count",
            value=context.guild.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{len(context.guild.channels)}"
        )
        embed.add_field (
          name="Owner", 
          value=context.guild.owner
        )
        embed.add_field(
            name=f"Roles ({len(context.guild.roles)})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {context.guild.created_at}"
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    @checks.not_blacklisted()
    async def ping(self, context: Context) -> None:
        embed = discord.Embed(
            title="<:zxtng_pepePing:1019273564886679592> Pong!",
            description=f"The bot latency is **{round(self.bot.latency * 1000)}ms.**",
            color=0xDA004E
        )
        message = await context.send("**pong 🏓**wait a sec <:silly_AE:1030269250524430450>..") 
        time.sleep(1.0)
        await message.edit(embed=embed,content=None)
      
    @commands.hybrid_command(
        name="invite",
        description="Get the invite link of the bot to be able to invite it.",
    )
    @checks.not_blacklisted()
    async def invite(self, context: Context) -> None:
        """
        Get the invite link of the bot to be able to invite it.
        
        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?&client_id={self.bot.config['application_id']}&scope=bot+applications.commands&permissions={self.bot.config['permissions']}).",
            color=0xD75BF4
        )
        try:
            # To know what permissions to give to your bot, please see here: https://discordapi.com/permissions.html and remember to not give Administrator permissions.
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="server",
        description="Get the invite link of the discord server of the bot for some support.",
    )
    @checks.not_blacklisted()
    async def server(self, context: Context) -> None:
        embed = discord.Embed(
            description=f"Join the support server for the bot by clicking [here](https://discord.gg/4RpR86WasS).",
            color=0xD75BF4
        )
        try:
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)
    @commands.hybrid_command(
        name="avatar",
        aliases=["av", "pfp"], 
        description="Get avatar of the user.",
        )
    @checks.not_blacklisted()
    async def avatar(self, context: Context, member: discord.User,hide:bool):
       if member == None:

            embed=discord.Embed(
            color=0xDA004E
            )
            embed.set_author(
              name=f"{context.author.name}'s avatar"
            )
            embed.set_image(
              url=context.author.avatar
            ) 
            await context.send(embed=embed)
       if hide == True:
            embed1 = discord.Embed(
              color=0xDA004E
            ) 
            embed1.set_author(
              name=f"{member.name}'s avatar"
            )
            embed1.set_image(
              url=member.avatar
            )
            await context.send(embed=embed1,ephemeral=True)
       else:
            embed1 = discord.Embed(
              color=0xDA004E
            ) 
            embed1.set_author(
              name=f"{member.name}'s avatar"
            )
            embed1.set_image(
              url=member.avatar
            )
            await context.send(embed=embed1)
         
    @commands.hybrid_command(
        name="8ball",
        description="Ask any question to the bot.",
    )
    @checks.not_blacklisted()
    @app_commands.describe(question="The question you want to ask.")
    async def eight_ball(self, context: Context, *, question: str) -> None:
        """
        Ask any question to the bot.
        
        :param context: The hybrid command context.
        :param question: The question that should be asked by the user.
        """
        answers = ["It is certain.", "It is decidedly so.", "You may rely on it.", "Without a doubt.",
                   "Yes - definitely.", "As I see, yes.", "Most likely.", "Outlook good.", "Yes.",
                   "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
                   "Cannot predict now.", "Concentrate and ask again later.", "Don't count on it.", "My reply is no.",
                   "My sources say no.", "Outlook not so good.", "Very doubtful."]
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{random.choice(answers)}",
            color=0xDA004E
        )
        embed.set_footer(
            text=f"The question was: {question}"
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="bitcoin",
        description="Get the current price of bitcoin.",
    )
    @checks.not_blacklisted()
    async def bitcoin(self, context: Context) -> None:
        """
        Get the current price of bitcoin.
        
        :param context: The hybrid command context.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.coindesk.com/v1/bpi/currentprice/BTC.json") as request:
                if request.status == 200:
                    data = await request.json(
                        content_type="application/javascript")  # For some reason the returned content is of type JavaScript
                    embed = discord.Embed(
                        title="Bitcoin price",
                        description=f"The current price is **${data['bpi']['USD']['rate']} :dollar:**",
                        color=0xDA004E
                    )
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                await context.send(embed=embed)
    @commands.hybrid_command(
        name="whois",
        description="Get some information about the user.",
    )
    @checks.not_blacklisted()
    async def whois(self, context: Context, user: discord.User, hide: bool) -> None:      
        embed = discord.Embed(
            color=0xDA004E
        )
        embed.set_author(
            name=f"{user.name}'s information"
        ) 
        embed.set_thumbnail(
          url=str(user.avatar.url)
        )
        embed.add_field(
            name="User name",
            value=user.name,
            inline=True
        )
        embed.add_field(
            name="tag",
            value=f"{user.discriminator}",
            inline=True
        )
        embed.add_field(
            name="Bot? ",
            value=user.bot,
        )
        embed.add_field(
            name="User ID",
            value=user.id,
            inline=False
        )
        embed.add_field(
            name="Account created",    
        value=user.created_at.strftime(
"%d/%m/%Y, %H:%M:%S"
        ), 
            inline=True
        ) 
        embed.add_field(
            name="Joined the server",
      value=user.joined_at.strftime(
              "%d/%m/%Y, %H:%M:%S"
        ),
            inline=True
        ) 
        embed.set_footer(
              text=f"Requested by {context.author}"
            )
        if hide == True:
          await context.send(embed=embed,ephemeral=True)
        else:
          await context.send(embed=embed)
      
    @commands.hybrid_command(
        name="emoji",
        description="Detail of the emoji.",
     ) 
    @checks.not_blacklisted()
    async def emoji(self, context: Context, emoji: discord.PartialEmoji) -> None:      

        embed = discord.Embed(
            color=0xDA004E
        )
        embed.set_author(
            name="Emoji Info"
        ) 
        embed.set_thumbnail(
            url=str(emoji.url)
        )
        embed.add_field(
            name="Name",
            value=emoji.name,
            inline=True
       )
        embed.add_field(
            name="ID",
            value=emoji.id,
            inline=True
       )   
        embed.add_field(
            name="Animated? ",
            value=emoji.animated,
            inline=True
       )
        await context.send(embed=embed)

    @commands.hybrid_command(
      name="dm",
      description="Dm a user"
    )
    @commands.has_permissions(administrator=True)
    @checks.not_blacklisted()
    async def dm(context:Context,message: discord.Message, user: discord.User,
                 msg: str) -> None:
          await user.send(msg)
          await message.send("Done")
                   
    @commands.hybrid_command(
        name="vote",
        description="Get the top.gg vote link of bot.",
    )
    @checks.not_blacklisted()
    async def vte(self, context: Context) -> None:
        embed = discord.Embed(
            description=f" Vote me on [here](https://top.gg/bot/830294601737961522/vote)",
            color=0xD75BF4
        )
        await context.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))
