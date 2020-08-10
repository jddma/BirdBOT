import discord
from discord.ext import commands


class Admin(commands.Cog):

    def __init__(self, bot):
        self.__bot = bot

    #Comando que sirve para asignar un rol a un usuario, para ejecutarlo el miembro debe tener el permiso de administración de roles
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def setrole(self, ctx, member_mention, role_mention):
        member = discord.utils.get(ctx.guild.members, mention=member_mention)
        role = discord.utils.get(ctx.guild.roles, mention=role_mention)

        #Se asegura que el miembro y el rol enviados existan en el servidor
        if (member is None) or (role is None):
            embed = discord.Embed(title="Error", description="Argumentos incorrectos", color=discord.Color.red())
            await ctx.send(embed=embed)

        else:
            #En caso de que el bot no tenga los permisos para realizar la acción
            try:
                await member.add_roles(role)
                embed = discord.Embed(title="Rol asignado", description=f"Al miembro {member_mention} se le ha asignado el rol {role_mention}", color=discord.Color.green())
                await ctx.send(embed=embed)

            except discord.errors.Forbidden:
                embed = discord.Embed(title="Error", description="No tengo permisos suficientes para esto", color=discord.Color.red())
                await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unsetrole(self, ctx, member_mention, role_mention):
        member = discord.utils.get(ctx.guild.members, mention=member_mention)
        role = discord.utils.get(ctx.guild.roles, mention=role_mention)

        # Se asegura que el miembro y el rol enviados existan en el servidor
        if (member is None) or (role is None):
            embed = discord.Embed(title="Error", description="Argumentos incorrectos", color=discord.Color.red())
            await ctx.send(embed=embed)

        else:
            # En caso de que el bot no tenga los permisos para realizar la acción
            try:
                await member.remove_roles(role)
                embed = discord.Embed(title="Rol asignado",
                                      description=f"Al miembro {member_mention} se le ha intentado retirado el rol {role_mention}",
                                      color=discord.Color.green())
                await ctx.send(embed=embed)

            except discord.errors.Forbidden:
                embed = discord.Embed(title="Error", description="No tengo permisos suficientes para esto",
                                      color=discord.Color.red())
                await ctx.send(embed=embed)