import discord
from discord.ext import commands
from constants.blacklist import BLACKLIST

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='sudo ', intents=intents)

# -------------------------------------------------------------------------------
message_logs = {}

#region Mensajes eliminados
@bot.event
async def on_message_delete(message):
    for log in message_logs.get(message.channel.name, []):
        if log["content"] == message.content and log["author"] == message.author.name:
            log["deleted"] = True
            break


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Moderación de mensajes
    if any(word in message.content for word in BLACKLIST):
        await message.delete()
        return

    # Guardar mensajes para logging
    if message.channel.name not in message_logs:
        message_logs[message.channel.name] = []

    message_logs[message.channel.name].append({
        "content": message.content,
        "author": message.author.name,
        "timestamp": message.created_at.isoformat(),
        "deleted": False
    })

    await bot.process_commands(message)
# -------------------------------------------------------------------------------