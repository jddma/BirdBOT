import discord
from discord.ext import commands


class Events(commands.Cog):

    def __init__(self, bot):
        self.__bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("El bot funciona")
        await self.__bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a ti bb"))

    @commands.Cog.listener()
    async def on_member_join(self, guild):
        print("member")
