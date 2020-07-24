import discord
from discord.ext import commands


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