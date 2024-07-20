import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='sudo ', intents=intents)

@bot.command()
async def reboot(ctx):
    await ctx.send(f'No, {ctx.author.mention}, no podes hacer un reboot a un Bot.')

bot.run(os.getenv('DISCORD_TOKEN'))
