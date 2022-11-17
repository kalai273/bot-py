import discord
import time
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks
from discord.ui import button

class helpselect(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=10)
      
        
        
    @discord.ui.select(placeholder="Select a module...",min_values=1,max_values=1,options=[
        discord.SelectOption(label="General",description="General Commands for some knowledge",emoji="<:thinkx:1019277696787816509>"),
        discord.SelectOption(label="Moderation",description="Moderation commands to help you moderate your server",emoji="<:moderation:939448699757666304>",value="1"), 
        discord.SelectOption(label="Utility",description="Utility commands for your server",emoji="<:utility:939449283378311168>"),
        discord.SelectOption(label="Gif",description="Part of fun commands related to images",emoji="🖼️"),
        
        discord.SelectOption(label="Fun",description="Fun commands to entertain you",emoji="<:fun:941216105769336913>"),
        discord.SelectOption(label="Owner",description="Emoji related commands",emoji="<:blob:956918297406898236>"),
        ])
    async def callback(self,select, i:discord.MessageInteraction):
        embed1=discord.Embed(
          title ="",
          color=0xfc03a5
        )
        embed1.add_field(name= "Moderation Command",value=f"""
 `❯ .kick` 
Kick a user out of the server.

 `❯ .nick`
Change the nickname of a user on a server.

 `❯ .ban`
Bans a user from the server.

 `❯ .warn`
Warns a user in the server.

 `❯ .warnings`
Shows the warnings of a user in the server.

 `❯ .purge`
 Delete a number of messages.
 
 `❯ .hackban`
Bans a user without the user having to be in the server.""")
        embed2=discord.Embed(color=0xfc03a5)
        embed2.add_field(name="Utility Commands",value=f"""
`❯ .whois`
 Get some information about the user.
   
`❯ .emoji`
 Detail of the emoji.

`❯ .server`
 Get the invite link of the discord server of the bot for some support.
   
`❯ .avatar`
 Get avatar of the user.
 
 `❯ .botinfo`
 Get some useful (or not) information about the bot.
   
`❯ .serverinfo`
 Get some useful (or not) information about the server.

`❯ .poll`
 poll for voting.
   
`❯ .servericon`
 avatar of the server.
""")
        embed6=discord.Embed(color=0xfc03a5)
        embed6.add_field(name="General",value=f"""
`❯ .help`
 List all commands the bot has loaded.
 
`❯ .ping`
 Check if the bot is alive.
 
`❯ .invite`
 Get the invite link of the bot to be able to invite it.
 
`❯ .8ball`
 Ask any question to the bot.
 
`❯ .bitcoin`
 Get the current price of bitcoin.

""")
        embed3=discord.Embed(color=0xfc03a5)
        embed3.add_field(name="Gif Commands",value="""
`❯ .kiss`
kiss your friend.

`❯ .slap`
slap your friend.

`❯ .punch`
punch your friend.

`❯ .hug`
hug your friend.

`❯ .cuddle`
cuddle your friend.

""")
        embed4=discord.Embed(color=0xfc03a5)
        embed4.add_field(name="Owner Commands",value="""
`❯ .sync`
 Synchronizes the slash commands.
 
`❯ .unsync`
 Unsynchonizes the slash commands.
 
`❯ .load`
 Load a cog
 
`❯ .unload`
 Unloads a cog.
 
`❯ .reload`
 Reloads a cog.
 
`❯ .shutdown`
 Make the bot shutdown.
 
`❯ .say`
 The bot will say anything you want.
 
`❯ .embed`
 The bot will say anything you want, but within embeds.
 
`❯ .blacklist`
 Get the list of all blacklisted users.
 
""")
        embed5=discord.Embed(color=0xfc03a5)
        embed5.add_field(name="Fun Commands",value=f"""
`❯ .randomfact`
 Get a random fact.
   
`❯ .coinflip`
 Make a coin flip, but give your bet before.

`❯ .reverse`
 The bot will reverse your message.

`❯ .rps`
 Play the rock paper scissors game against the bot.
   
`❯ .simp`
 simp meter.
   
`❯ .pp`
 How long is your shlong? 😳

`❯ .hot`
 claculating hot ❤💕💖%
""")

        if i.values[0] == "1":
            await select.response.edit_message(embed=embed1)
        elif i.values[0] == "Utility":
            await select.response.edit_message(embed=embed2)
        elif i.values[0] == "General":
            await select.response.edit_message(embed=embed6)
        elif i.values[0] == "Gif":
            await select.response.edit_message(embed=embed3)
        elif i.values[0] == "Owner":
            await select.response.edit_message(embed=embed4)
        elif i.values[0] == "Fun":
            await select.response.edit_message(embed=embed5)
"""
    async def on_timeout(self, select : discord.ui.Select, i : discord.Interaction):
        self.placeholder="Disabled due to timeout!" 
        self.disabled = True
"""
class Util(commands.Cog, name="util"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="help",
        aliases=["h","hel"], 
        description="List all commands the bot has loaded."
    )
    @checks.not_blacklisted()
    async def t(self, context: Context) -> None:
        embed=discord.Embed(
          title="Commands of Arti",
          description="**Please select a category to view all its commands**",
          color=0xfc03a5
        )
        embed.set_footer(
          icon_url=context.author.avatar,
          text=f"Requested by {context.author}"
        )
        view = helpselect()
        await context.send(embed=embed,view=view)
    


async def setup(bot):
    await bot.add_cog(Util(bot))
