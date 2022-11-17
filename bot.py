import asyncio
import json
import os
import platform
import random
import sqlite3
import time
import sys

from contextlib import closing

import discord
from discord import Interaction
from discord.ext import tasks, commands
from discord.ext.commands import Bot
from discord.ext.commands import Context
import exceptions

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

intents = discord.Intents.all()
intents.members = True

#bot = Bot(command_prefix=commands.when_mentioned_or(config["prefix"]),
         # intents=intents,
         # help_command=None)

intents.message_content = True

def get_prefix(client,message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    return [prefixes[str(message.guild.id)]]

def when_mentioned_or_function(func):
    def inner(bot, message):
        r = func(bot, message)
        r = commands.when_mentioned(bot, message) + r
        return r
    return inner

bot = commands.Bot(command_prefix=when_mentioned_or_function(get_prefix),intents=intents,help_command=None)


@bot.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "."
    with open("prefixes.json", "w") as f:
        json.dump(prefixes,f)

def init_db():
    with closing(connect_db()) as db:
        with open("database/schema.sql", "r") as f:
            db.cursor().executescript(f.read())
        db.commit()


def connect_db():
    return sqlite3.connect("database/database.db")


bot.config = config
bot.db = connect_db()


@bot.event
async def on_ready() -> None:
    """
    The code in this even is executed when the bot is ready
    """
    print(f"Logged in as {bot.user.name}")
    print("-------------------")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=f"{len(bot.users)} users in {len(bot.guilds)} servers"))

    await bot.tree.sync()


@bot.event
async def on_message(message: discord.Message) -> None:
    if message.content == bot.user.mention:
      with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
        prefix=prefixes[str(message.guild.id)]
        embed=discord.Embed(
          description=f"my prefix of this server is **`{prefix}`**", 
          color=0xDA004E
        )
        await message.channel.send(embed=embed)

    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)


"""
@bot.command()
async def afk(ctx, mins):
    current_nick = ctx.author.nick
    await ctx.send(f"{ctx.author.mention} has gone afk for {mins} minutes.")
    await ctx.author.edit(nick=f"[AFK]{ctx.author.name}")

    counter = 0
    while counter <= int(mins):
        counter += 1
        await asyncio.sleep(60)
        if ctx.author.mention==True:
          await ctx.send("hi")
        if counter == int(mins):
            await ctx.author.edit(nick=current_nick)
            await ctx.send(f"{ctx.author.mention} is no longer AFK")
            break
"""
@bot.command(
  name="ser"
)
async def cm(ctx, guild_id: str):
      guild = bot.get_guild(int(guild_id))
      channel = guild.channels[0]
      invitelink = await channel.create_invite(max_uses=1)
      await ctx.send(invitelink)

@bot.event
async def on_command_completion(context: Context) -> None:
    """
    The code in this event is executed every time a normal command has been *successfully* executed
    :param context: The context of the command that has been executed.
    """
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    if context.guild is not None:
        channel = bot.get_channel(1018179637207117885)
        await channel.send(
            f"**Executed {executed_command} command in {context.guild.name} ({context.channel.name}) by {context.author} (ID: {context.author.id})**"
        )
    else:
        await channel.send(
            f"**Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs**"
        )


@bot.event
async def on_command_error(context: Context, error) -> None:
    """
    The code in this event is executed every time a normal valid command catches an error
    :param context: The context of the normal command that failed executing.
    :param error: The error that has been faced.
    """
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            title="Hey, please slow down!",
            description=
            f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B)
        await context.send(embed=embed)
    elif isinstance(error, exceptions.UserBlacklisted):
        """
        The code here will only execute if the error is an instance of 'UserBlacklisted', which can occur when using
        the @checks.not_blacklisted() check in your command, or you can raise the error by yourself.
        """
        embed = discord.Embed(
            title="Error!",
            description="You are blacklisted from using the bot.",
            color=0xE02B2B)
        await context.reply(embed=embed)
    elif isinstance(error, exceptions.UserNotOwner):
        """
        Same as above, just for the @checks.is_owner() check.
        """
        embed = discord.Embed(title="Error!",
                              description="You are not the owner of the bot!",
                              color=0xE02B2B)
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description=
            " <a:error:1020525852670296134>You are missing the permission(s) `"
            + ", ".join(error.missing_permissions) +
            "` to execute this command!",
            color=0xE02B2B)
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            # We need to capitalize because the command arguments have no capital letter in the code.
            description=str(error).capitalize(),
            color=0xE02B2B)
        await context.send(embed=embed)
    raise error


async def load_cogs() -> None:
    """
    The code in this function is executed whenever the bot will start.
    """
    for file in os.listdir(f"./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


init_db()
asyncio.run(load_cogs())
bot.run(os.environ['token'])
