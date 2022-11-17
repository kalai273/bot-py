import discord
import pytz
import datetime
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks
class Utility(commands.Cog, name="utility"):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="poll",
        description="poll for voting.",
    )
    @checks.not_blacklisted()
    async def poll(self, context: Context, *, title):
        embed = discord.Embed(title="poll",
                              description=f"{title}",
                              color=0xDA004E)
        embed.set_footer(text=f" asked by {context.message.author}!")
        embed_message = await context.send(embed=embed)
        await embed_message.add_reaction(
            "\<a:Cutie_Verifiedtick:1021065282179055706>")
        await embed_message.add_reaction("\<a:error:1020525852670296134>")
        await embed_message.add_reaction("🤷")

    @commands.hybrid_command(
        name="servericon",
        description="avatar of the server.",
    )
    @checks.not_blacklisted()
    async def server_avatar(self, ctx: Context):
        """ Get the current server icon """
        if not ctx.guild.icon:
            return await ctx.send("This server does not have an icon...")

        format_list = []
        formats = ["JPEG", "PNG", "WebP"]
        if ctx.guild.icon.is_animated():
            formats.append("GIF")

        for img_format in formats:
            format_list.append(
                f"[{img_format}]({ctx.guild.icon.replace(format=img_format.lower(), size=1024)})"
            )

        embed = discord.Embed()
        embed.set_image(
            url=f"{ctx.guild.icon.with_size(256).with_static_format('png')}")
        embed.title = "Icon formats"
        embed.description = " **-** ".join(format_list)
        await ctx.send(f"🖼 Icon to **{ctx.guild.name}**", embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
