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

    @commands.command()
    async def tournend(self, ctx):
        try:
            del self.__tournaments[ctx.guild.id]
            embed = discord.Embed(title="Eliminado")
            pass
        except:
            embed = discord.Embed(title="Error", description="No se registra ningún torneo en progreso", color=discord.Color.red())
            ctx.send(embed=embed)

    @commands.command()
    async def tournament(self, ctx, channel_to_search: str):
        try:
            self.__tournaments[ctx.guild.id]
            embed = discord.Embed(title="Torneo en progreso", description="Ya existe un torneo activo en el servidor, si quieres eliminarlo usa el comando `tournend`.", color=discord.Color.dark_orange())
            await ctx.send(embed=embed)
        except:
            channel, err = self.__search_channel(ctx.guild.channels, channel_to_search)
            if err:
                embed = discord.Embed(title="Error", description=f"No existe el servidor {channel_to_search}", color=discord.Color.red())
                await ctx.send(embed=embed)
            else:
                channel_members = self.__get_channel_members(channel)
                if len(channel_members) < 2:
                    embed = discord.Embed(title="Alakesad", description="Que solo debes estar para querer hacer un torneo tu solo",color=discord.Color.blue())
                    embed.set_thumbnail(url="https://pbs.twimg.com/media/ENKYaSZWoAInZ6G.jpg")
                    await ctx.send(embed=embed)
                else:
                    if len(channel_members) % 2 != 0:
                        channel_members.append("repechaje")
                    self.__tournaments[ctx.guild.id] = channel_members
                    self.__tournaments[ctx.guild.id] = random.sample(self.__tournaments[ctx.guild.id], len(self.__tournaments[ctx.guild.id]))
                    embed = discord.Embed(title="NUEVO TORNEO", description="Ronda 1", color=discord.Color.dark_gold())
                    i = 0
                    while i < len(self.__tournaments[ctx.guild.id]):
                        embed.add_field(name="*", value=f"{self.__tournaments[ctx.guild.id][i]} vs {self.__tournaments[ctx.guild.id][i + 1]}")
                        i += 2
                    await ctx.send(embed=embed)