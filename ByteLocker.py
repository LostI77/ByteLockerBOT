from dotenv import load_dotenv
import discord
from discord.ext import commands
import json
import os
import yt_dlp as youtube_dl
import aiohttp

load_dotenv()  # Cargar variables del archivo .env

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='-', intents=intents)

# Palabras malsonantes y listas negras de spam
BLACKLIST = ["badword1", "badword2", "spamlink.com"]

# Almacenar mensajes
message_logs = {}

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

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

@bot.event
async def on_message_delete(message):
    for log in message_logs.get(message.channel.name, []):
        if log["content"] == message.content and log["author"] == message.author.name:
            log["deleted"] = True
            break

@bot.command()
async def logs(ctx, action, channel_name=None):
    if action == "dump" and channel_name:
        channel_logs = message_logs.get(channel_name, [])
        with open(f'{channel_name}_logs.json', 'w') as f:
            json.dump(channel_logs, f, indent=4)
        await ctx.send(f'Logs del canal {channel_name} guardados en {channel_name}_logs.json')
    elif action == "list" and channel_name == "channels":
        await ctx.send(f'Canales registrados: {", ".join(message_logs.keys())}')

@bot.command()
async def play(ctx, url):
    if not ctx.voice_client:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("Debes estar en un canal de voz para reproducir música.")
            return

    ctx.voice_client.stop()
    ffmpeg_options = {
        'options': '-vn'
    }
    ydl_opts = {
        'format': 'bestaudio',
        'noplaylist': 'True',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        ctx.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=url2, **ffmpeg_options))

    await ctx.send(f'Reproduciendo: {url}')

@bot.command()
async def skip(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("Canción saltada.")
    else:
        await ctx.send("No hay ninguna canción en reproducción.")

@bot.command()
async def scanurl(ctx, url):
    # Usar VirusTotal API para escanear la URL (requiere una clave de API)
    api_key = os.getenv("VIRUSTOTAL_TOKEN")
    scan_url = f"https://www.virustotal.com/api/v3/urls"
    headers = {
        "x-apikey": api_key
    }
    data = {
        "url": url
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(scan_url, headers=headers, data=data) as resp:
            if resp.status == 200:
                result = await resp.json()
                await ctx.send(f'Resultado del escaneo de URL: {json.dumps(result, indent=4)}')
            else:
                await ctx.send("Error al escanear la URL.")

@bot.command()
async def scanfile(ctx):
    if len(ctx.message.attachments) == 0:
        await ctx.send("No se ha adjuntado ningún archivo para escanear.")
        return

    file_url = ctx.message.attachments[0].url
    file_name = ctx.message.attachments[0].filename

    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as resp:
            if resp.status == 200:
                file_data = await resp.read()

                # Usar VirusTotal API para escanear el archivo (requiere una clave de API)
                api_key = os.getenv("VIRUSTOTAL_TOKEN")
                scan_url = f"https://www.virustotal.com/api/v3/files"
                headers = {
                    "x-apikey": api_key
                }
                files = {
                    "file": (file_name, file_data)
                }

                async with session.post(scan_url, headers=headers, data=files) as scan_resp:
                    if scan_resp.status == 200:
                        result = await scan_resp.json()
                        await ctx.send(f'Resultado del escaneo del archivo: {json.dumps(result, indent=4)}')
                    else:
                        await ctx.send("Error al escanear el archivo.")

bot.run(os.getenv('DISCORD_TOKEN'))
