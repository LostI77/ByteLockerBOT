import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='sudo ', intents=intents)

@bot.command(name="whome")
async def whome(ctx):
    await ctx.send(f'{ctx.author.mention}')

bot.run(os.getenv('DISCORD_TOKEN'))
