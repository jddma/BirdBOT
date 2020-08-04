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

    def __get_member(self, members, winner):
        for member in members:
            if member.mention == winner:
                return member, False

        return None, True

    #Metodo que genera la nueva vista del torneo o mustra el campeón
    def __get_round_embed(self, ctx):

        #obtiene la cantdad de eliminados en la ronda actual
        count_lousers = self.__tournaments[ctx.guild.id].count("~~Eliminado~~")

        #Verifica que la ronda halla terminado con el numero de eliminados
        if count_lousers == (len(self.__tournaments[ctx.guild.id]) / 2):
            #elimina definitivamente a los eliminados para pasar a la siguiente ronda
            for _ in range(count_lousers):
                self.__tournaments[ctx.guild.id].remove("~~Eliminado~~")

            #rectifica que se tenga que añadir un repechaje
            if ((len(self.__tournaments[ctx.guild.id]) % 2) != 0) and (len(self.__tournaments[ctx.guild.id]) > 1):
                self.__tournaments[ctx.guild.id].append("repechaje")

        #rectifica que exista un campeón
        if len(self.__tournaments[ctx.guild.id]) == 1:
            winner, err = self.__get_member(ctx.guild.members, self.__tournaments[ctx.guild.id][0])
            if not err:
                #Mostrar el campeón en el chat
                embed = discord.Embed(title="CAMPEÓN",
                                      description=f":confetti_ball::confetti_ball::confetti_ball:{self.__tournaments[ctx.guild.id][0]}:confetti_ball::confetti_ball::confetti_ball:",
                                      color=discord.Color.gold())
                #En caso de que el ganador no sea un usuario de Discord
                try:
                    embed.set_image(url=winner.avatar_url)
                except:
                    embed.set_image(url="https://cdn.discordapp.com/embed/avatars/2.png")

                embed.set_thumbnail(url="https://media1.tenor.com/images/8fd803044e63b141814db1650c35ee43/tenor.gif")
                del self.__tournaments[ctx.guild.id]
                return embed
        #final
        elif len(self.__tournaments[ctx.guild.id]) == 2:
            desc = "Final"
        #semifinañ
        elif len(self.__tournaments[ctx.guild.id]) == 4:
            desc = "Semifinal"
        else:
            desc = "Ronda"

        embed = discord.Embed(title="Torneo", description=desc, color=discord.Color.dark_gold())
        i = 0
        #genera los enfrentamientos
        while i < len(self.__tournaments[ctx.guild.id]):
            embed.add_field(name="*", value=f"{self.__tournaments[ctx.guild.id][i]} ***vs*** {self.__tournaments[ctx.guild.id][i + 1]}")
            i += 2
        embed.set_thumbnail(url=ctx.guild.icon_url)
        return embed

    def __get_command_error_embed(self, command, command_args, ctx):
        embed = discord.Embed(title="Error", description="Comando usado erroneamente", color=discord.Color.red())
        embed.add_field(name=f"Uso del comando _{command}_", value=f"{command} {command_args}")
        embed.set_thumbnail(url=ctx.me.avatar_url)
        return embed

    #Comando que permite añadir manualmente un participante a un torneo en curso
    @commands.command()
    async def tournadd(self, ctx, member_to_add):

        #Rectifica que el participante a agregar no sea el participante reservado "repechaje"
        if member_to_add == "repechaje":
            embed = discord.Embed(title="Error",description="El participante __repechaje__ no puede ser usado, por favor use otro nombre", color=discord.Color.red())
            await ctx.send(embed=embed)

        else:
            try:
                #Rectifica que el perticipante a agregar no se encuantre ya en el torneo
                if member_to_add in self.__tournaments[ctx.guild.id]:
                    embed = discord.Embed(title="Error", description=f"El participante {member_to_add} ya se encuentra en el torneo", color=discord.Color.red())
                    await ctx.send(embed=embed)
                #Si existe un repechaje en el torneo se reemplazara con el nuevo participante
                else:
                    rep_index = self.__tournaments[ctx.guild.id].index("repechaje")
                    self.__tournaments[ctx.guild.id][rep_index] = member_to_add
                    await ctx.send(embed=self.__get_round_embed(ctx))
            #En caso de que en la ronda actual no existe ningun repechaje añadira al nuevo participante y un repechaje
            except ValueError:
                self.__tournaments[ctx.guild.id].extend([member_to_add, "repechaje"])
                await ctx.send(embed=self.__get_round_embed(ctx))

            #En caso de que no exista un torneo activo en el servidor
            except KeyError:
                embed = discord.Embed(title="Error", description="No existe un torneo activo en el servidor", color=discord.Color.red())
                await ctx.send(embed=embed)

    @tournadd.error
    async def tournadd_error(self, ctx, error):
        if error.args[0] == 'member_to_add is a required argument that is missing.':
            await ctx.send(embed=self.__get_command_error_embed("tournadd", "<miembro_a_agregar>", ctx))

    #Comando que sirve para poner el reemplazar el ganador de un repechaje
    @commands.command()
    async def tournrep(self, ctx, rep_member_to_add):
        #En caso de que no exista un torneo activo en el servidor
        try:
            #Obtiene la posición del repqchaje
            rep_index = self.__tournaments[ctx.guild.id].index("repechaje")

            #en caso de que no exisa un repechaje en la ronda actual
            if rep_index == -1:
                embed = discord.Embed(title="No repechaje", description="No existe un repechaje en la ronda actual", color=discord.Color.red())
                await ctx.send(embed=embed)
            else:
                 self.__tournaments[ctx.guild.id][rep_index] = rep_member_to_add
                 await ctx.send(embed=self.__get_round_embed(ctx))
        except KeyError:
            embed = discord.Embed(title="Torneo inexistente", description="No existe un torneo activo en el servidor", color=discord.Color.red())
            await ctx.send(embed=embed)

    @tournrep.error
    async def tournrep_error(self, ctx, error):
        if error.args[0] == 'rep_member_to_add is a required argument that is missing.':
            await ctx.send(embed=self.__get_command_error_embed("tournrep", "<miembro_a_reemplazar por el repechaje>", ctx))

    #Comando para registrar la derrota de un jugador
    @commands.command()
    async def tournloser(self, ctx, louser: str):
        #Obtener el id del servidor sonde se uso el comando
        id_server = ctx.guild.id

        #Rectifica que exista un torneo activo en el servidor
        try:

            #Rectifica que el participante a eliminar este activo en el torneo
            if louser in self.__tournaments[id_server]:
                #Elimina al participante y muestra el estado del torneo
                louser_index = self.__tournaments[id_server].index(louser)
                self.__tournaments[id_server][louser_index] = "~~Eliminado~~"
                await ctx.send(embed=self.__get_round_embed(ctx))
            else:
                embed = discord.Embed(title="No encontrado", description=f"El participante {louser} no se encuentra en el torneo o ya fue eliminado", color=discord.Color.red())
                await ctx.send(embed=embed)
        except KeyError:
            embed = discord.Embed(title="Torneo inexsistente", description=f"No existe un torneo activo en el servidor, para crearlo use el comando `tournament`", color=discord.Color.red())
            await ctx.send(embed=embed)

    @tournloser.error
    async def tournloser_error(self, ctx, error):
        if error.args[0] == 'louser is a required argument that is missing.':
            await ctx.send(embed=self.__get_command_error_embed("tournloser", "<miembro_a_eliminar>", ctx))

    #Comando para eliminar un torneo del servidor
    @commands.command()
    async def tournend(self, ctx):

        #En caso de no encontrar un torneo existente lo informara
        try:
            del self.__tournaments[ctx.guild.id]
            embed = discord.Embed(title="Eliminado", description="Torneo eliminado")
            await ctx.send(embed=embed)
        except KeyError:
            embed = discord.Embed(title="Error", description="No se registra ningún torneo en progreso", color=discord.Color.red())
            await ctx.send(embed=embed)

    # Comando para la cración de un torneo, se le debe enviar como parametro el canal del cual se obtendran los participantes
    @commands.command()
    async def tournament(self, ctx, *, channel_to_search: str):

        #Verifica qu un torneo no se encuentre en progreso
        try:
            self.__tournaments[ctx.guild.id]
            embed = discord.Embed(title="Torneo en progreso", description="Ya existe un torneo activo en el servidor, si quieres eliminarlo usa el comando `tournend`.", color=discord.Color.dark_orange())
            await ctx.send(embed=embed)
        except KeyError:
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

    @tournament.error
    async def tournament_error(self, ctx, error):
        if error.args[0] == 'channel_to_search is a required argument that is missing.':
            await ctx.send(embed=self.__get_command_error_embed("tournament", "<canal_de_donde_se_obtendran_participantes>", ctx))