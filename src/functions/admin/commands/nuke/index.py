import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='sudo ', intents=intents)

@bot.command()
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

bot.run(os.getenv('DISCORD_TOKEN'))
