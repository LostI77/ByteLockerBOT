from discord.ext import commands

class Nuke(commands.Cog):
    @commands.command()
    @commands.has_role("Co-founder")
    async def nuke(ctx):
        # Elimina todos los mensajes del canal actual.
        await ctx.message.delete()
        await ctx.channel.purge()
        await ctx.send(f"Nuked by {ctx.author.mention}")

    @nuke.error
    async def nuke_error(ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("No tienes permiso para usar este comando.")

async def setup(bot):
    await bot.add_cog(Nuke(bot))