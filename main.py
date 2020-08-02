from discord.ext import commands

from util.settings import Vars

from cogs.basic import BasicCommands
from cogs.events import Events
from cogs.tournament import Tournament
from cogs.admin import Admin

class BirdBOT(commands.Bot):

    def __init__(self):
        self.vars = Vars()
        super().__init__(command_prefix=self.vars.get_prefix())

        #Agregar los cogs correspondientes
        self.add_cog(BasicCommands(self, self.vars.get_sounds()))
        self.add_cog(Events(self))
        self.add_cog(Tournament(self))
        self.add_cog(Admin(self))


if __name__ == '__main__':
    bot = BirdBOT()
    bot.run(bot.vars.get_token())