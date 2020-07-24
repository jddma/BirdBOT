import discord
from discord.ext import commands

import requests

from bs4 import BeautifulSoup

class BasicCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Funcionando")

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(title=f"{ctx.guild.name}", description="Bird bot versión de mierda",color=discord.Color.blue())
        embed.add_field(name="ID del servidor", value=f"{ctx.guild.id}")
        embed.add_field(name="Servidor creado el", value=f"{ctx.guild.created_at}")
        embed.add_field(name="Dueño del servidor", value=f"{ctx.guild.owner}")
        embed.add_field(name="Región del servidor", value=f"{ctx.guild.region}")
        embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
        await ctx.send(embed=embed)

    @commands.command()
    async def img(self, ctx, *, search):
        url = f"https://www.google.co.in/search?q={search}&source=lnms&tbm=isch"

        page = requests.get(url)
        if page.status_code == 200:
            embed = discord.Embed(title=search, color=discord.Color.dark_magenta())
            page = BeautifulSoup(page.text, "lxml")
            img = page.find("img", attrs={"class": "t0fcAb"})
            embed.set_image(url=f"{img.get('src')}")
            await ctx.send(embed=embed)