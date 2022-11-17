import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.utils import get

from helpers import checks


class Choice(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        

    @discord.ui.button(label="Heads", style=discord.ButtonStyle.blurple)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = "heads"
        self.stop()
      
    @discord.ui.button(label="Tails", style=discord.ButtonStyle.blurple)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = "tails"
        self.stop()


class RockPaperScissors(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Scissors", description="You choose scissors.", emoji="✂"
            ),
            discord.SelectOption(
                label="Rock", description="You choose rock.", emoji="🪨"
            ),
            discord.SelectOption(
                label="paper", description="You choose paper.", emoji="🧻"
            ),
        ]
        super().__init__(
            placeholder="Choose...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        choices = {
            "rock": 0,
            "paper": 1,
            "scissors": 2,
        }
        user_choice = self.values[0].lower()
        user_choice_index = choices[user_choice]

        bot_choice = random.choice(list(choices.keys()))
        bot_choice_index = choices[bot_choice]

        result_embed = discord.Embed(color=0xDA004E)
        result_embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)

        if user_choice_index == bot_choice_index:
            result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0xF59E42
        elif user_choice_index == 0 and bot_choice_index == 2:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0xDA004E
        elif user_choice_index == 1 and bot_choice_index == 0:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0xDA004E
        elif user_choice_index == 2 and bot_choice_index == 1:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0xDA004E
        else:
            result_embed.description = f"**I won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0xE02B2B
        await interaction.response.edit_message(embed=result_embed, content=None, view=None)


class RockPaperScissorsView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(RockPaperScissors())


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="randomfact",
        description="Get a random fact."
    )
    @checks.not_blacklisted()
    async def randomfact(self, context: Context) -> None:
        """
        Get a random fact.
        
        :param context: The hybrid command context.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(
                        description=data["text"],
                        color=0xD75BF4
                    )
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                await context.send(embed=embed)

    @commands.hybrid_command(
        name="coinflip",
        description="Make a coin flip, but give your bet before."
    )
    @checks.not_blacklisted()
    async def coinflip(self, context: Context) -> None:
        """
        Make a coin flip, but give your bet before.
        
        :param context: The hybrid command context.
        """
        buttons = Choice()
        embed = discord.Embed(
            description="What is your bet?",
            color=0xDA004E
        )
        message = await context.send(embed=embed, view=buttons)
        await buttons.wait()  # We wait for the user to click a button.
        result = random.choice(["heads", "tails"])
        print(buttons.value)
        if buttons.value == result:
            embed = discord.Embed(
                description=f"Correct! You guessed `{buttons.value}` and I flipped the coin to `{result}`.",
                color=0x9C84EF
            )
        else:
            embed = discord.Embed(
                description=f"Woops! You guessed `{buttons.value}` and I flipped the coin to `{result}`, better luck next time!",
                color=0xE02B2B
            )
        await message.edit(embed=embed, view=None, content=None)

    @commands.hybrid_command(
        name="choose",
        aliases=["choice"],
        description=" I will choose best option for you"
    )
    async def choose(self, ctx: commands.Context, *, options: str):
        items = [
            option.strip().replace("*","") for option in options.split(",")
        ]
        choice = random.choice(items)
        await ctx.send(f"**{choice}**")

  
    @commands.hybrid_command(
        name="reverse",
        description="The bot will reverse your message.",
    )
    async def say(self, context: Context, * , message: str) -> None:
        await context.send(message[::-1])
      
    @commands.hybrid_command(
        name="rps",
        description="Play the rock paper scissors game against the bot."
    )
    @checks.not_blacklisted()
    async def rock_paper_scissors(self, context: Context) -> None:
        """
        Play the rock paper scissors game against the bot.
        
        :param context: The hybrid command context.
        """
        view = RockPaperScissorsView()
        await context.send("Please make your choice", view=view)

    @commands.hybrid_command()
    async def _dm(ctx, guild_id: str):
      guild = self.bot.get_guild(int(guild_id))
      channel = guild.channels[0]
      invitelink = await channel.create_invite(max_uses=1)
      await ctx.author.send(invitelink)
  
    @commands.hybrid_command(
        name="simp",
        description="simp meter."
    )
    @checks.not_blacklisted()
    async def simp(self, ctx: Context, member: discord.User) -> None:
      
      embed = discord.Embed(
        color=0xDA004E
     )        
      if member is None or member.id == ctx.author.id:
            embed.title = f"You are {random.randrange(0, 101)}% a simp \U0001f927"
      else:
            embed.title = f"{member.name} is {random.randrange(0, 101)}% a simp \U0001f927"

      await ctx.channel.send(embed=embed)

    @commands.hybrid_command(
        name="pp", 
        description="How long is your shlong? \U0001f633"
        ) 
    @checks.not_blacklisted()
    async def pp(self, ctx: Context, member: discord.Member) -> None:
        choice = random.randrange(0, 17)
        embed = discord.Embed(
          color=0xDA004E
        )
        if choice <= 5:
            reply = "Damn that's awkward \U0001f480"
            value = f'8{"=" * choice}D\n{reply}'
        else:
              reply = "Keep it up king \U0001f60e"
              
        if   member is None or member.id == ctx.author.id:
                    embed.add_field(
                        name=f"Your pp size \U0001f633", value= f'8{"=" * choice}D\n{reply}'
                        )
        else:
                            embed.add_field(
                                name=f"{member.name}'s pp size \U0001f633",     value= f'8{"=" * choice}D\n{reply}'
                                )
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="hot",
        aliases=["hotc","hotcalc"], 
        description="claculating hot ❤💕💖%"
        ) 
    @checks.not_blacklisted()
    async def hotcalc(self, ctx, *, user: discord.Member = None):
        """ Returns a random percent for how hot is a discord user """
        user = user or ctx.author
        
        random.seed(user.id)
        r = random.randint(25, 100)
        hot = r /1.23
            
        if hot > 75:
          emoji = "💞"
        elif hot > 50:
          emoji = "💖"
        elif hot > 25:
          emoji = "❤"
        else:
          emoji = "💔"
        if ctx.author.id == 911892459695505429:
          await ctx.send(f"You are **99.99%** hot 💞")
          return False
        if user.id == 911892459695505429:
          await ctx.send(f"{user.name}** 99.99%** hot 💞")
        elif user == ctx.author:
          await ctx.reply(f"You are **{hot:.2f}%** hot {emoji}")
          return
        else:
          await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")
      

async def setup(bot):
    await bot.add_cog(Fun(bot))
