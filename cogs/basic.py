import discord
from discord.ext import commands

import time

from random import randrange

import requests

import asyncio

from bs4 import BeautifulSoup


class BasicCommands(commands.Cog):

    def __init__(self, bot):
        self.__bot = bot

    #Comando que permite verificar el ping que presenta la conexión
    @commands.command()
    async def ping(self, ctx):
        """ Pong! """
        before = time.monotonic()
        message = await ctx.send("Pong!")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong!  `{int(ping)}ms`")

    #Comando para mostrar información del servidor
    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(title=f"{ctx.guild.name}", description="Bird bot versión de mierda",color=discord.Color.blue())
        embed.add_field(name="ID del servidor", value=f"{ctx.guild.id}")
        embed.add_field(name="Servidor creado el", value=f"{ctx.guild.created_at}")
        embed.add_field(name="Dueño del servidor", value=f"{ctx.guild.owner}")
        embed.add_field(name="Región del servidor", value=f"{ctx.guild.region}")
        embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
        await ctx.send(embed=embed)

    #Comando para buscar y mostrar en el chat una imagen
    """@commands.command()
    async def img(self, ctx, *, search):
    
        #Definir la URL de búsqueda de google pasando como parametro de búsqueda
        url = f"https://www.google.co.in/search?q={search}&source=lnms&tbm=isch"

        #Realiza la slicitud
        page = requests.get(url)
        if page.status_code == 200:
            embed = discord.Embed(title=search, color=discord.Color.dark_magenta())
            page = BeautifulSoup(page.text, "lxml")
            
            #Obtiene la primera imagen obtenida
            img = page.find("img", attrs={"class": "t0fcAb"})
            embed.set_image(url=f"{img.get('src')}")
            await ctx.send(embed=embed)"""

    #Comando que se ejecuta una acción despues de 40 segundos
    @commands.command()
    async def deathnote(self, ctx, user):
        embed = discord.Embed(title="Dead", description=f"Alguien ha matado a {user}",color=discord.Color.red())
        embed.set_image(url="https://pa1.narvii.com/6039/bc4e95759f014c1aa5a8bf465ed6cf0db6156a1e_hq.gif")
        await asyncio.sleep(40)
        await ctx.send(embed=embed)

    #Comando que escoge aleatoriamente entre varias opciones
    @commands.command()
    async def random(self, ctx, *, options_str):
        options = options_str.split(" ")
        result = options[randrange(len(options))]
        embed = discord.Embed(title="Random", description=result, color=discord.Color.dark_magenta())
        await ctx.send(embed=embed)