import discord
from discord.ext import commands


class logs(commands.Cog, name="logs"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        logs = self.bot.get_channel(1026167599953870958)
        embed = discord.Embed(title=f"Joined Guild: {guild.name}", color=0x7EEBEB)
        embed.add_field(
          name="Name/ID", value=f"{guild.name} (`{guild.id}`)", inline=True
        )
        embed.add_field(
            name="Server Owner",
            value=f"{guild.owner} (`{guild.owner.id}`)",
            inline=True,)
        integrations = await guild.integrations()
        for integration in integrations:
           if isinstance(integration, discord.BotIntegration):
             if integration.application.user.name == self.bot.user.name:
               embed.add_field(name="Inviter",value=integration.user)
               break
        embed.add_field(
            name="Server Created On", value=f"{guild.created_at} UTC", inline=True
        )
        embed.add_field(name="Member Count", value=f"{guild.member_count}", inline=True)
        embed.set_thumbnail(url=guild.icon)
        await logs.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        embed = discord.Embed(title=f"Left Guild: {guild.name}", color=0x7EEBEB)
        embed.add_field(
            name="Name/ID", value=f"{guild.name} (`{guild.id}`)", inline=True
        )
        embed.add_field(
            name="Server Owner",
            value=f"{guild.owner} (`{guild.owner.id}`)",
            inline=True,
        )
        embed.add_field(
            name="Server Created On", value=f"{guild.created_at} UTC", inline=True
        )
        embed.add_field(name="Member Count", value=f"{guild.member_count}", inline=True)
        embed.set_thumbnail(url=guild.icon)
        logs = self.bot.get_channel(1026167599953870958) #Channel ID
        await logs.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self,message: discord.Message): 
     channel = self.bot.get_channel(1020559800553181215)
     if message.guild is None and message.author != self.bot.user:
        embed = discord.Embed(
        color=0xfff00
       )
        embed.add_field (
        name="dm msg:", 
        value=message.content
      )
        embed.set_footer(
        text= f"| sent by {message.author.name}",
        icon_url=message.author.avatar
      )
        await channel.send(embed=embed)
        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_message_delete(self,message):
     embed=discord.Embed(title=f"{message.author}deleted a message",color=0xDA00F)
     embed.add_field(
      name= message.content,
      value=f"""**```
server : {message.guild}
channel: #{message.channel}```**
      
      """,
      inline=True)
     embed.set_footer(
      text=message.author
      ) 
     channel=self.bot.get_channel(1021976074785144902)
     await channel.send(embed=embed)
       
async def setup(bot):
    await bot.add_cog(logs(bot))