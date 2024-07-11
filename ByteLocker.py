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
# Canal donde se enviarán las respuestas para revisión si el puntaje es bajo
REVIEW_CHANNEL_ID = 1260581358380646451  # Reemplaza con el ID del canal de revisión

# Preguntas 
questions = {
    "¿Pregunta 1?\n1. Lorem ipsum\n2. Dolor sit amet\n3. Consectetur\n4. Adipiscing elit": (2, 20),  # (Correct answer, points)
    "¿Pregunta 2?\n1. Sed do eiusmod\n2. Tempor incididunt\n3. Ut labore et dolore\n4. Magna aliqua": (2, 30),
    "¿Pregunta 3?\n1. Ut enim ad minim\n2. Veniam, quis nostrud\n3. Exercitation ullamco\n4. Laboris nisi": (2, 25),
    # Add more questions in the same format
}

# Canal donde se enviarán las preguntas a los nuevos miembros
WELCOME_CHANNEL_ID = 1260581245822435370  # Reemplaza con el ID del canal de bienvenida

# Verificar la conexión
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignorar mensajes propios
    
    log_command(message)  
    await bot.process_commands(message)

def log_command(message):
    if message.content.startswith(bot.command_prefix):  # Checkea si es un comando
        command_name = message.content.split()[0][len(bot.command_prefix):]
        print(f"Command '{command_name}' triggered by {message.author} in {message.channel}")


async def conduct_survey(member, channel):
    total_score = 0
    responses = []

    def check(m):
        return m.author == member and m.channel == channel and m.content.isdigit() and 1 <= int(m.content) <= 4

    for question, (correct_answer, points) in questions.items():
        await channel.send(question)
        try:
            msg = await bot.wait_for('message', check=check, timeout=60)
            user_answer = int(msg.content)
            responses.append((question, user_answer))
            if user_answer == correct_answer:
                total_score += points  # Suma puntos con las repuesta correctas
        except asyncio.TimeoutError:
            await channel.send(f'{member.mention}, no respondiste a tiempo. Intenta nuevamente.')
            return

    # Envía las respuestas
    review_channel = bot.get_channel(REVIEW_CHANNEL_ID)
    if review_channel:
        response_str = "\n".join([f"{q}: {r}" for q, r in responses])
        await review_channel.send(f'Respuestas de {member.mention}:\n{response_str}')

    # Asigna rol si aprobó
    if total_score >= 75:
        await channel.send(f'{member.mention}, ¡felicitaciones! Has pasado la encuesta con {total_score} puntos.')
        # Asigna rol
        role_id = 1260594141629382666  
        role = channel.guild.get_role(role_id) 
        if role:
            await member.add_roles(role)
            await channel.send(f'Te he asignado el rol {role.name}.')
        else:
            await channel.send('No se pudo encontrar el rol especificado.')
        await channel.send(f'{member.mention}, tus respuestas están siendo revisadas por un administrador. Obtuviste {total_score} puntos.')

# @bot.event
# async def on_member_join(member):
#     welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)
#     if welcome_channel is not None:
#         await welcome_channel.send(f'¡Bienvenido {member.mention}! Responde las siguientes preguntas:')
#         await conduct_survey(member, welcome_channel)

@bot.command(name='encuesta')
async def start_survey(ctx):
    print("Encuesta command triggered!") 
    await ctx.send(f'{ctx.author.mention}, iniciaré la encuesta contigo.')
    print(f"Comando encuesta iniciado por {ctx.author}")
    await conduct_survey(ctx.author, ctx.channel)

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('pong')
    
def log_command(message):
    if message.content.startswith(bot.command_prefix):  # Checkea si es un comando
        command_name = message.content.split()[0][len(bot.command_prefix):]
        print(f"Command '{command_name}' triggered by {message.author} in {message.channel}")


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
async def scanip(ctx, ip):
    # Escanear una IP con VirusTotal
    api_key = os.getenv('VIRUSTOTAL_TOKEN')
    scan_ip = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {
        'accept': 'application/json',
        'x-apikey': api_key
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(scan_ip, headers=headers) as resp:
            if resp.status == 200:
                result = await resp.json()
                resumen = f"IP: {ip}\n"
                resumen += f"Puntuación de VirusTotal: {result.get('data', {}).get('attributes', {}).get('last_analysis_stats', {}).get('malicious', 0)}\n"
                await ctx.send(resumen)
            else:
                await ctx.send("Error al escanear la IP.")


@bot.command()
async def scanurl(ctx, url):
    # Usar VirusTotal API para escanear la URL (requiere una clave de API)
    api_key = os.getenv("VIRUSTOTAL_TOKEN")
    scan_url = f"https://www.virustotal.com/api/v3/domains/{url}"
    headers = {
        'accept': 'application/json',
        'x-apikey': api_key
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
                    'accept': 'application/json',
                    'x-apikey': api_key               
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
