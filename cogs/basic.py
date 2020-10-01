import discord
from discord.ext import commands

import time

from random import randrange

import requests

import asyncio

from bs4 import BeautifulSoup


class BasicCommands(commands.Cog):

    def __init__(self, bot, sounds):
        self.__bot = bot
        self.__sounds = sounds
        self.__votings = {}

    def __get_channel_of_server(self, voice_clients, server_id):
        for client in voice_clients:
            if client.server_id == server_id:
                return client, False

        return None, True

    #Comando que permite verificar el ping que presenta la conexión
    @commands.command()
    async def ping(self, ctx):
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
        await ctx.message.delete()
        await asyncio.sleep(40)
        await ctx.send(embed=embed)

    #Metodo que se ejecutara cuando el comando deathbote falle
    @deathnote.error
    async def deathnote_error(self, ctx, error):
        if error.args[0] == 'user is a required argument that is missing.':
            embed = discord.Embed(title="Error", description="Comando usado erroneamente", color=discord.Color.red())
            embed.add_field(name="Uso del comando _deathnote_", value="deathnote <member>")
            embed.set_thumbnail(url=ctx.me.avatar_url)
            await ctx.send(embed=embed)

    #Comando que escoge aleatoriamente entre varias opciones
    @commands.command()
    async def random(self, ctx, *, options_str):
        options = options_str.split(" ")
        result = options[randrange(len(options))]
        embed = discord.Embed(title="Random", description=result, color=discord.Color.dark_magenta())
        await ctx.send(embed=embed)

    # Metodo que se ejecutara cuando el comando error falle
    @random.error
    async def random_error(self, ctx, error):
        t = error.args[0]
        if error.args[0] == 'options_str is a required argument that is missing.':
            embed = discord.Embed(title="Error", description="Comando usado erroneamente", color=discord.Color.red())
            embed.add_field(name="Uso del comando _random_", value="random <opcion1 opcion2 opcion3 ...>")
            embed.set_thumbnail(url=ctx.me.avatar_url)
            await ctx.send(embed=embed)

    #Comando para reproducir los sonidos configurados
    @commands.command()
    async def sound(self, ctx, *, sound):

        #Rectifica que el usuario que ejecuto el comando se encuantre en un canal de voz
        if ctx.author.voice is None:
            embed = discord.Embed(title="Error", description="Debe estar en un vanal de voz para esto", color=discord.Color.red())
            await ctx.send(embed=embed)

        else:
            try:
                sound_file_name = self.__sounds[sound]
                sound_file_path = f"resources/sounds/{sound_file_name}"
                channel_name = ctx.author.voice.channel.name
                channel = discord.utils.get(ctx.guild.channels, name=channel_name)

                #Verifica que el bot ya se encuentre en un canal del servidor
                try:
                    vc = await channel.connect()

                except discord.errors.ClientException:
                    vc, _ = self.__get_channel_of_server(ctx.bot.voice_clients, ctx.guild.id)

                    #Rectifica que el bot se encuentre en el mismo canar que el usuario
                    if not channel.id == vc.channel.id:
                        await vc.disconnect()
                        vc = await channel.connect()

                #Rectifica que no exista un sonido ya reproduciendose
                try:
                    vc.play(discord.FFmpegPCMAudio(sound_file_path), after=None)
                    embed = discord.Embed(title="Sound", description=f"Reproduciendo _{sound}_", color=discord.Color.blue())
                    await ctx.send(embed=embed)

                except discord.errors.ClientException:
                    embed = discord.Embed(title="Ocupado", description="Ya se encuantra un sonido e reproducción",color=discord.Color.red())
                    await ctx.send(embed=embed)

            except KeyError:
                embed = discord.Embed(title="Not Found", description=f"El sonido _{sound}_ no se encuentra", color=discord.Color.red())
                await ctx.send(embed=embed)

    @sound.error
    async def sound_error(self, ctx, error):
        if error.args[0] == 'sound is a required argument that is missing.':
            embed = discord.Embed(title="Error", description="Comando usado erroneamente", color=discord.Color.red())
            embed.add_field(name="Uso del comando _sound_", value="sound <nombre_del_sonido>")
            embed.set_thumbnail(url=ctx.me.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def soundslist(self, ctx):
        sounds = self.__sounds.keys()
        if len(sounds) == 0:
            embed = discord.Embed(title="Sin contenido", description="NO se tiene sonidos registrados", color=discord.Color.red())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="__Listas de sonidos__", color=discord.Color.blue())
            embed.set_thumbnail(url=ctx.me.avatar_url)
            for sound_name in sounds:
                embed.add_field(name=sound_name, value=self.__sounds[sound_name])

            await ctx.send(embed=embed)

    @commands.command()
    async def voting(self, ctx, num: int, *, options):

        #Verifica que no exista una votación en progreso
        try:
            self.__votings[ctx.guild.id]
            embed = discord.Embed(title="Votación en progrado", description="Ya existe una votación en progreso", color=discord.Color.red())
            await ctx.send(embed=embed)
        except KeyError:
            #Obtiene las opciones ingresadas
            options_list = options.split(" ")

            #Instancia un contador para cada opción
            options_count = [0, ] * len(options_list)
            voting = [options_list, options_count, num, []]
            embed = discord.Embed(title="Votación iniciada", description="", color=discord.Color.green())
            for i in range(len(options_list)):
                embed.add_field(name=f"Opción #{i}: ", value=options_list[i])

            self.__votings[ctx.guild.id] = voting
            await ctx.send(embed=embed)

    @commands.command()
    async def vote(self, ctx, option: int):

        #Validar que exista una votación en progreso
        try:

            #Validar que el miembro que uso el comando no realizara una votación previamente
            if ctx.author.mention in self.__votings[ctx.guild.id][3]:
                embed = discord.Embed(title="NO mi ciela", description="usted ya puso su voto", color=discord.Color.red())
                await ctx.send(embed=embed)

            else:

                #Suma el voto
                self.__votings[ctx.guild.id][1][option] += 1

                #Registrar el usuario que ya realizo un voto
                self.__votings[ctx.guild.id][3].append(ctx.author.mention)
                await ctx.send("Voto realizado")

                #Validar que todos los votos se hayan realizado
                if len(self.__votings[ctx.guild.id][3]) == self.__votings[ctx.guild.id][2]:
                    embed = discord.Embed(title="Votación finalizada", description="Resultaodos: ",color=discord.Color.gold())
                    for i in range(len(self.__votings[ctx.guild.id][0])):
                        option = self.__votings[ctx.guild.id][0][i]
                        count = self.__votings[ctx.guild.id][1][i]
                        embed.add_field(name="Resultados", value=f"{option}: {count}")

                    del self.__votings[ctx.guild.id]
                    await ctx.send(embed=embed)


        except KeyError as err:
            print(err)
            embed = discord.Embed(title="Votación inexsistente", description="No existe una votación en progreso", color=discord.Color.red())

            await ctx.send(embed=embed)
