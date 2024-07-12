from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
import json
import os
import yt_dlp as youtube_dl
import aiohttp
import asyncio
import random
import os
import subprocess

load_dotenv()  # Cargar variables del archivo .env

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='sudo ', intents=intents)
BLACKLISTED_COMMANDS = [
    "more", "less", "head", "tail", "echo",  # Comandos de lectura
    "sudo", "rm", "chmod", "chown", "kill",  # Comandos de administración de sistema
    "wget", "curl", "nc",  # Comandos de red
    "bash", "sh", "python", "perl", "ruby",  # Intérpretes de comandos y lenguajes de scripting
]
#ALLOWED_COMMANDS = ["ls", "pwd", "whoami"]  # Lista blanca de comandos permitidos

BLACKLIST = ["badword1", "badword2", "spamlink.com", "acortar.link", "bit.ly", "adf.ly"]


#region Preguntas
questions = {
    # Preguntas fáciles
    "¿Cuál es el puerto predeterminado para HTTPS?\n1. 80\n2. 443\n3. 22\n4. 25": (2, 10),
    "¿Qué herramienta se utiliza comúnmente para realizar un escaneo de puertos en una red?\n1. Nmap\n2. Wireshark\n3. Metasploit\n4. Burp Suite": (1, 10),
    "¿Qué tipo de ataque implica la inserción de código malicioso en las consultas SQL?\n1. Cross-Site Scripting (XSS)\n2. Ataque de diccionario\n3. Inyección SQL\n4. Phishing": (3, 10),
    "¿Qué protocolo se utiliza para asegurar la comunicación en una red Wi-Fi?\n1. WEP\n2. WPA2\n3. WPA\n4. WPA3": (4, 10),
    "¿Qué significa 'DoS' en el contexto de ciberseguridad?\n1. Defacement of Service\n2. Denial of Service\n3. Data over Security\n4. Distribution of Service": (2, 10),
    "¿Cuál es el propósito de un firewall?\n1. Bloquear el acceso físico al servidor\n2. Monitorear y controlar el tráfico de red entrante y saliente\n3. Analizar y escanear vulnerabilidades\n4. Realizar copias de seguridad de datos": (2, 10),
    "¿Qué es una VPN?\n1. Virtual Public Network\n2. Virtual Private Network\n3. Visual Private Network\n4. Visual Public Network": (2, 10),
    "¿Qué es un ataque de fuerza bruta?\n1. Probar todas las combinaciones posibles de una clave\n2. Inyectar código malicioso\n3. Monitorear el tráfico de red\n4. Redirigir el tráfico de red a otro servidor": (1, 10),
    # Preguntas de dificultad media
    "¿Qué técnica utiliza el análisis de las frecuencias de uso de palabras o frases para decodificar mensajes cifrados?\n1. Fuerza bruta\n2. Criptoanálisis\n3. Ataque de diccionario\n4. Ingeniería social": (2, 20),
    "¿Cuál es el propósito del uso de un honeypot en una red?\n1. Aumentar la velocidad de la red\n2. Atraer y analizar comportamientos de atacantes\n3. Filtrar el tráfico de red\n4. Cifrar la comunicación": (2, 20),
    "¿Qué algoritmo de cifrado utiliza una clave pública y una clave privada para cifrar y descifrar datos?\n1. AES\n2. DES\n3. RSA\n4. MD5": (3, 20),
    "¿Cuál es la diferencia principal entre un ataque de tipo 'buffer overflow' y un 'heap overflow'?\n1. Ubicación en la memoria\n2. Tipo de datos afectados\n3. Tamaño del desbordamiento\n4. Modo de explotación": (1, 20),
    "¿Qué significa 'XSS' en el contexto de ciberseguridad?\n1. Cross-Site Scripting\n2. XML Secure Script\n3. Cross-Server Security\n4. Xtreme Secure Scripting": (1, 20),
    "¿Qué es una botnet?\n1. Una red de robots\n2. Una red de computadoras infectadas controladas remotamente\n3. Un programa para eliminar virus\n4. Una técnica de cifrado": (2, 20),
    "¿Qué protocolo se utiliza para cifrar correos electrónicos?\n1. SSL\n2. TLS\n3. PGP\n4. FTP": (3, 20),
    "¿Qué es un certificado digital?\n1. Un archivo que contiene virus\n2. Un documento que certifica la identidad de una persona o entidad\n3. Un protocolo de red\n4. Un algoritmo de cifrado": (2, 20),
    # Preguntas difíciles
    "¿Cuál es la longitud mínima recomendada para una clave RSA segura en la actualidad?\n1. 1024 bits\n2. 2048 bits\n3. 3072 bits\n4. 4096 bits": (2, 30),
    "¿Qué protocolo es utilizado por los sistemas de detección de intrusos basados en red (NIDS) para capturar y analizar el tráfico?\n1. SNMP\n2. NetFlow\n3. PCAP\n4. IPFIX": (3, 30),
    "¿Qué técnica criptográfica se utiliza en el protocolo TLS para asegurar la integridad y autenticidad de los datos?\n1. Criptografía asimétrica\n2. Funciones hash\n3. Cifrado simétrico\n4. Firmas digitales": (4, 30),
    "¿Cuál de los siguientes métodos es más seguro para el intercambio de claves en un entorno inseguro?\n1. Intercambio de claves Diffie-Hellman\n2. Intercambio de claves RSA\n3. Intercambio de claves ECC\n4. Intercambio de claves DSA": (3, 30),
    "¿Qué herramienta se utiliza para realizar fuzzing en aplicaciones con el objetivo de encontrar vulnerabilidades?\n1. Nessus\n2. Burp Suite\n3. AFL (American Fuzzy Lop)\n4. Nikto": (3, 30),
    "¿Cuál es el propósito del uso de un ataque de relleno de Oracle en criptografía?\n1. Descifrar datos cifrados sin la clave\n2. Insertar datos maliciosos en una base de datos\n3. Manipular la autenticación basada en tokens\n4. Detectar ataques de fuerza bruta": (1, 30),
    "¿Qué es un ataque de canal lateral?\n1. Un ataque que aprovecha información física del sistema\n2. Un ataque a través de la red\n3. Un ataque a la interfaz de usuario\n4. Un ataque a través de software de terceros": (1, 30),
    "¿Cuál es la diferencia entre 'salt' y 'pepper' en criptografía?\n1. Salt es una cadena aleatoria añadida a la entrada; Pepper es una cadena aleatoria añadida al hash\n2. Salt es una cadena fija; Pepper es una cadena aleatoria\n3. Salt se añade antes del hash; Pepper se añade después\n4. Salt se usa para cifrar datos; Pepper se usa para descifrar datos": (1, 30),
    # Preguntas de C y C++
    "¿Cómo se le llama a una variable que almacena la dirección en memoria de otra variable en C y C++?\n1. Parámetro\n2. Referencia\n3. Puntero\n4. Ninguna de las anteriores": (3, 20),
    "¿Cómo se imprime 'Hola mundo' en Java?\n1. System.out.println(\"Hola mundo\");\n2. std::cout << \"Hola mundo\"\n3. print(\"Hola mundo\")\n4. Console.WriteLine(\"Hola mundo\")": (1, 30),
    "¿Cómo se le llama al valor que se le pasa a una función?\n1. Parámetro\n2. Referencia\n3. Variable\n4. Argumento": (4, 25),
    "¿Qué es un array?\n1. Una lista de valores de un mismo tipo\n2. Una estructura de datos que asocia una clave y un valor\n3. Una estructura compuesta de nodos": (1, 20),
    "¿Qué es una instancia?\n1. Un valor retornado desde una función\n2. Un tipo de dato primitivo\n3. Un objeto creado a partir de una clase": (3, 30),
    "¿Qué es un 'for'?\n1. Bucle que ejecuta un bloque de código una determinada cantidad de veces\n2. Un bucle que se ejecuta mientras una condición sea verdadera\n3. Una sentencia que evalúa el valor de una variable en casos": (1, 25),
    "¿Qué es un 'enum'?\n1. Una clase que recibe los atributos y métodos de otra\n2. Una estructura que contiene campos y funciones\n3. Una colección de funciones que pueden ser implementadas en una clase\n4. Una colección de constantes enumeradas": (4, 20),
    "¿Qué es un callback?\n1. Un puntero a una función\n2. Una función que es pasada como argumento a otra función\n3. Una función que retorna un valor": (2, 30),
    "¿Cuál es la extensión de un archivo de código de Python?\n1. .rs\n2. .cpp\n3. .js\n4. .py": (4, 25),

}

# -------------------------------------------------------------------------------
#region Noticias (Comentado)


# @tasks.loop(hours=1)  # Se ejecuta cada hora, ajusta la frecuencia según tus necesidades
# async def publicar_noticias():
#     news_channel_id = int(os.getenv('NEWS_CHANNEL_ID'))  # Convertir a entero
#     async with aiohttp.ClientSession() as session:
#         async with session.get('https://hacker-news.firebaseio.com/v0/topstories.json') as resp:
#             top_stories = await resp.json()
#         # Tomamos las 5 noticias más importantes
#         for story_id in top_stories[:5]:
#             async with session.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json') as resp:
#                 story = await resp.json()
#             # Verificamos si la noticia tiene título y URL
#             if 'title' in story and 'url' in story:
#                 canal = bot.get_channel(news_channel_id)
#                 if canal is not None:
#                     mensaje = f"**{story['title']}**\n{story['url']}"
#                     await canal.send(mensaje)
#                     await asyncio.sleep(1)  # Pequeña pausa para evitar sobrecargar la API
#                 else:
#                     print(f"Error: No se encontró el canal con ID {news_channel_id}")

# -------------------------------------------------------------------------------
# @bot.command()
# @commands.has_role('Co-founder')
# async def bash(ctx, *, command):
#         if command.split()[0] not in BLACKLISTED_COMMANDS:  # Verifica si el comando está en la lista blanca
#             try:
#                 result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
#                 await ctx.send(f"Resultado:`\n\n{result}\n`")
#             except subprocess.CalledProcessError as e:
#                 await ctx.send(f"Error al ejecutar el comando: {e}")
#         else:
#             await ctx.send("El comando no está en la lista blanca.")
#region Encuesta
async def conduct_survey(member, channel):
    total_score = 0
    responses = []
    def check(m):
        return m.author == member and m.channel == channel and m.content.isdigit() and 1 <= int(m.content) <= 4
    # Selecciona 5 preguntas al azar
    selected_questions = random.sample(list(questions.items()), k=5)
    for question, (correct_answer, points) in selected_questions:
        await channel.send(question)
        try:
            msg = await bot.wait_for('message', check=check, timeout=60)
            try:
                user_answer = int(msg.content) 
                responses.append((question, user_answer))
                if user_answer == correct_answer:
                    total_score += points
            except ValueError:
                await channel.send(f'{member.mention}, por favor introduce un número válido entre 1 y 4.')
        except asyncio.TimeoutError:
            await channel.send(f'{member.mention}, no respondiste a tiempo. Intenta nuevamente.')
            return


    # Envía las respuestas
    review_channel = bot.get_channel(int(os.getenv('REVIEW_CHANNEL_ID')))
    print(f"review_channel: {review_channel}")
    if review_channel:
        response_str = "\n".join([f"{q}: {r}" for q, r in responses])
        await review_channel.send(f'Respuestas de {member.mention}:\n{response_str}')

    # Asigna rol si aprobó
    if total_score >= 75:
        await channel.send(f'{member.mention}, ¡felicitaciones! Has pasado la encuesta con {total_score} puntos.')
        # Asigna rol
        role_id = int(os.getenv('VERIFIED_ROLE'))
        print(f"role_id: {role_id}")
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
#region Iniciar Encuesta
@bot.command(name='encuesta')
async def start_survey(ctx):
    print("Encuesta command triggered!") 
    await ctx.send(f'{ctx.author.mention}, iniciaré la encuesta contigo.')
    print(f"Comando encuesta iniciado por {ctx.author}")
    await conduct_survey(ctx.author, ctx.channel)

# -------------------------------------------------------------------------------
#region Verificar conexión
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    news_channel_id = int(os.getenv('NEWS_CHANNEL_ID'))  # Convertir a entero el ID del canal
    canal = bot.get_channel(news_channel_id)
    if canal is not None:
        print(f"Canal de noticias encontrado: {canal.name}")
       # publicar_noticias.start()
    else:
        print(f"Error: No se encontró el canal con ID {news_channel_id}")


#region Mute
@bot.command()
@commands.has_role('Co-founder')
@commands.has_permissions(manage_roles=True) # Requiere permiso para gestionar roles
async def mute(ctx, member: discord.Member, *, reason=None):
    # ID del rol a quitar (reemplázalo con el ID correcto)
    rol_a_quitar_id = int(os.getenv('VERIFIED_ROLE'))
    
    # ID del rol a asignar (reemplázalo con el ID correcto)
    rol_a_asignar_id =  int(os.getenv('MUTED_ROLE_ID'))
    
    rol_a_quitar = ctx.guild.get_role(rol_a_quitar_id)
    rol_a_asignar = ctx.guild.get_role(rol_a_asignar_id)
    if rol_a_quitar and rol_a_asignar:
        await member.remove_roles(rol_a_quitar, reason=reason)
        await member.add_roles(rol_a_asignar, reason=reason)
        await ctx.send(f"{member.mention} ha sido silenciado.")
    else:
        await ctx.send("Error: No se encontraron los roles especificados.")

@mute.error
async def logs_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("No tienes permiso para usar este comando.")
# -------------------------------------------------------------------------------
@bot.command()
@commands.has_role('Co-founder')
@commands.has_permissions(manage_roles=True) # Requiere permiso para gestionar roles
async def unmute(ctx, member: discord.Member, *, reason=None):
    # ID del rol a quitar (el que se asignó al mutear)
    rol_a_quitar_id = int(os.getenv('MUTED_ROLE_ID'))
    
    # ID del rol a asignar (el que se quitó al mutear)
    rol_a_asignar_id = int(os.getenv('VERIFIED_ROLE'))
    rol_a_quitar = ctx.guild.get_role(rol_a_quitar_id)
    rol_a_asignar = ctx.guild.get_role(rol_a_asignar_id)
    if rol_a_quitar and rol_a_asignar:
        await member.remove_roles(rol_a_quitar, reason=reason)
        await member.add_roles(rol_a_asignar, reason=reason)
        await ctx.send(f"{member.mention} ha sido desmuteado.")
    else:
        await ctx.send("Error: No se encontraron los roles especificados.")

@unmute.error
async def logs_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("No tienes permiso para usar este comando.")

#region Logs
message_logs = {}
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
#region Mensajes eliminados
@bot.event
async def on_message_delete(message):
    for log in message_logs.get(message.channel.name, []):
        if log["content"] == message.content and log["author"] == message.author.name:
            log["deleted"] = True
            break

# -------------------------------------------------------------------------------
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
#region Música (WIP)
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

# -------------------------------------------------------------------------------

@bot.command()
async def skip(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("Canción saltada.")
    else:
        await ctx.send("No hay ninguna canción en reproducción.")

# -------------------------------------------------------------------------------
#region Virustotal IP Scan
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

# -------------------------------------------------------------------------------
#region Nuke
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

# -------------------------------------------------------------------------------
#region Virustotal Domain Scan
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

# -------------------------------------------------------------------------------
#region Virustotal File Scan
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

# -------------------------------------------------------------------------------
@bot.command()
async def whoami(ctx):
    await ctx.send(f'{ctx.author.mention}')

@bot.command()
async def reboot(ctx):
    await ctx.send(f'No, {ctx.author.mention}, no podes hacer un reboot a un Bot.')


@bot.command()
async def passwd(ctx):
    await ctx.send("""`root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
user:x:1000:1000::/home/user:/bin/bash
nixbld1:x:30001:30000:Nix build user 1:/var/empty:/sbin/nologin`""")


bot.run(os.getenv('DISCORD_TOKEN'))
