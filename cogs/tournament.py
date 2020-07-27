import random

import discord
from discord.ext import commands

class Tournament(commands.Cog):

    def __init__(self, bot):
        self.__bot = bot
        self.__tournaments = {}

    def __search_channel(self, channels, search):
        for channel in channels:
            if channel.name == search:
                return channel, False

        return None, True

    def __get_channel_members(self, channel):
        result = []
        for member in channel.members:
            if not member.bot:
                result.append(member.mention)

        return result

    def __get_round_embed(self, ctx):
        if len(self.__tournaments[ctx.guild.id]) == 1:
            pass
        elif len(self.__tournaments[ctx.guild.id]) == 2:
            desc = "Final"
        elif len(self.__tournaments[ctx.guild.id]) == 4:
            desc = "Semifinal"
        else:
            desc = "Ronda"

        embed = discord.Embed(title="Torneo", description=desc, color=discord.Color.dark_gold())
        i = 0
        while i < len(self.__tournaments[ctx.guild.id]):
            embed.add_field(name="*", value=f"{self.__tournaments[ctx.guild.id][i]} ***vs*** {self.__tournaments[ctx.guild.id][i + 1]}")
            i += 2
        embed.set_thumbnail(url=ctx.guild.icon_url)
        return embed

    #Comando para eliminar un torneo del servidor
    @commands.command()
    async def tournend(self, ctx):

        #En caso de no encontrar un torneo existente lo informara
        try:
            del self.__tournaments[ctx.guild.id]
            embed = discord.Embed(title="Eliminado", description="Torneo eliminado")
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title="Error", description="No se registra ningún torneo en progreso", color=discord.Color.red())
            await ctx.send(embed=embed)

    # Comando para la cración de un torneo, se le debe enviar como parametro el canal del cual se obtendran los participantes
    @commands.command()
    async def tournament(self, ctx, channel_to_search: str):

        #Verifica qu un torneo no se encuentre en progreso
        try:
            self.__tournaments[ctx.guild.id]
            embed = discord.Embed(title="Torneo en progreso", description="Ya existe un torneo activo en el servidor, si quieres eliminarlo usa el comando `tournend`.", color=discord.Color.dark_orange())
            await ctx.send(embed=embed)
        except:
            #Llama al metodo encargado de buscar el canal solicitado
            channel, err = self.__search_channel(ctx.guild.channels, channel_to_search)

            #Verifica que el canal solicitado exista
            if err:
                embed = discord.Embed(title="Error", description=f"No existe el servidor {channel_to_search}", color=discord.Color.red())
                await ctx.send(embed=embed)
            else:
                #Llama al metodo enccargado de obtener los miembros no bots del canal solicitado
                channel_members = self.__get_channel_members(channel)

                #Verifica que en el canal solo se encuantre un miembro
                if len(channel_members) < 2:
                    embed = discord.Embed(title="Alakesad", description="Que solo debes estar para querer hacer un torneo tu solo",color=discord.Color.blue())
                    embed.set_thumbnail(url="https://pbs.twimg.com/media/ENKYaSZWoAInZ6G.jpg")
                    await ctx.send(embed=embed)
                else:
                    #Encaso de que el numero de participantes sea impar añadira un participante como repechaje
                    if len(channel_members) % 2 != 0:
                        channel_members.append("repechaje")

                    #Agrega el torneo correspondiente al servidor con sus participantes y los mezcla
                    self.__tournaments[ctx.guild.id] = channel_members
                    self.__tournaments[ctx.guild.id] = random.sample(self.__tournaments[ctx.guild.id], len(self.__tournaments[ctx.guild.id]))
                    await ctx.send(embed=self.__get_round_embed(ctx))