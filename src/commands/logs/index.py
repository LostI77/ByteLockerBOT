import discord
from discord.ext import commands
from ByteLocker import bot
import json
from messages.index import message_logs

#region Dump logs
@bot.command()
@commands.has_role("Co-founder")
async def logs(ctx, action, channel_name=None):
    if action == "dump" and channel_name:
        channel_logs = message_logs.get(channel_name, [])
        with open(f'{channel_name}_logs.json', 'w') as f:
            json.dump(channel_logs, f, indent=4)
        await ctx.send(f'Logs del canal {channel_name} guardados en {channel_name}_logs.json')
    elif action == "list" and channel_name == "channels":
        await ctx.send(f'Canales registrados: {", ".join(message_logs.keys())}')

@logs.error
async def logs_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("No tienes permiso para usar este comando.")

# -------------------------------------------------------------------------------