from discord.ext import commands
from constants.blacklist_commands import BLACKLISTED_COMMANDS
import subprocess

class Bash(commands.Cog):
    @commands.command()
    @commands.has_role('Co-founder')
    async def bash(ctx, *, command):
            if command.split()[0] not in BLACKLISTED_COMMANDS:  # Verifica si el comando está en la lista blanca
                try:
                    result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
                    await ctx.send(f"Resultado:`\n\n{result}\n`")
                except subprocess.CalledProcessError as e:
                    await ctx.send(f"Error al ejecutar el comando: {e}")
            else:
                await ctx.send("El comando no está en la lista blanca.")
    @bash.error
    async def bash_error(ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("No tienes los permisos necesarios para ejecutar este comando. Se requiere el rol 'Co-founder'.")
        else:
            await ctx.send("Ha ocurrido un error al intentar ejecutar el comando.")

async def setup(bot):
    await bot.add_cog(Bash(bot))