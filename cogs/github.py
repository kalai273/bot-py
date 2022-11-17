import json

import requests
from bs4 import BeautifulSoup
from discord.ext import commands

import discord

def createem(text,color=0x171515):
  
  return discord.Embed(description=text,color=color)

class GitHub(commands.Cog):
    pass

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
      name="githubrepo",
      aliases=['ghr'],
      description="Get the detais about github repository"
    )
    async def github(self, ctx, repo):
        """Fetch repository info"""

        req = requests.get(f'https://api.github.com/repos/{repo}')
        apijson = json.loads(req.text)
        if req.status_code == 200:
            em = discord.Embed(color=0x4078c0)
            em.set_author(name=apijson['owner']['login'], icon_url=apijson['owner']['avatar_url'],
                          url=apijson['owner']['html_url'])
            em.set_thumbnail(url=apijson['owner']['avatar_url'])
            em.add_field(name="Repository:", value=f"[{apijson['name']}]({apijson['html_url']})", inline=True)
            em.add_field(name="Language:", value=apijson['language'], inline=True)

            try:
                license_url = f"[{apijson['license']['spdx_id']}]({json.loads(requests.get(apijson['license']['url']).text)['html_url']})"
            except:
                license_url = "None"
            em.add_field(name="License:", value=license_url, inline=True)
            if apijson['stargazers_count'] != 0:
                em.add_field(name="Star:", value=apijson['stargazers_count'], inline=True)
            if apijson['forks_count'] != 0:
                em.add_field(name="Fork:", value=apijson['forks_count'], inline=True)
            if apijson['open_issues'] != 0:
                em.add_field(name="Issues:", value=apijson['open_issues'], inline=True)
            em.add_field(name="Description:", value=apijson['description'], inline=False)

            for meta in BeautifulSoup(requests.get(apijson['html_url']).text, features="html.parser").find_all('meta'):
                try:
                    if meta.attrs['property'] == "og:image":
                        em.set_thumbnail(url=meta.attrs['content'])
                        break
                except:
                    pass

            await ctx.send(embed=em)
        elif req.status_code == 404:
            """if repository not found"""
            await ctx.send(embed=createem('NOT FOUND'))
        elif req.status_code == 503:
            """GithubAPI down"""
            await ctx.send(embed=createem("GithubAPI down"))
            
        else:
            """some error occurred while fetching repository info"""
            await ctx.send(embed=createem('UNKNOWN ERROR'))
    @commands.hybrid_command(
      name="github",
      aliases=['gh'],
      description="Get the details github user."
    )
    async def githubuser(self, ctx, username):
        """Fetch user info"""

        req = requests.get(f'https://api.github.com/users/{username}')
        apijson = json.loads(req.text)
        if req.status_code == 200:
            em = discord.Embed(color=0x4078c0)
            em.add_field(name="Bio",value=f"```{apijson['bio']}```")
            em.add_field(name="User Info",value=f"** Realname** : _{apijson['name']}_\n **GitHub ID** : _{apijson['id']}_ \n **Location** :  _{apijson['location']}_ \n **Website** : _[click me]({apijson['blog']})_")

            em.add_field(name="Social Stats", value=f" **followers** : _{apijson['followers']}_ \n**following** : _{apijson['following']}_", inline=False)  
          
            em.set_author(name=f"{apijson['name']}", icon_url=apijson['avatar_url'],
                          url=apijson['html_url'])
            em.set_image(url=apijson['avatar_url'])
            em.set_thumbnail(url=apijson['avatar_url'])
            em.set_footer(text='Account created at '+apijson['created_at'])

            await ctx.send(embed=em)
        elif req.status_code == 404:
            """if user not found"""
            await ctx.send(embed=createem('NOT FOUND'))
        elif req.status_code == 503:
            """GithubAPI down"""
            await ctx.send(embed=createem("GithubAPI down"))
            
        else:
            """some error occurred while fetching repository info"""
            await ctx.send(embed=createem('UNKNOWN ERROR'))


async def setup(bot):
    """ Setup GitHub Module"""
    await bot.add_cog(GitHub(bot))