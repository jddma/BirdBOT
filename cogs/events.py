from discord.ext import commands


class Events(commands.Cog):

    def __init__(self, bot):
        self.__bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("El bot funciona")

    @commands.Cog.listener()
    async def on_member_join(self, guild):
        pass
