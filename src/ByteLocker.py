from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
import os
import subprocess
from constants.questions import questions
from commands.surveys.index import conduct_survey, start_survey

load_dotenv()  # Cargar variables del archivo .env

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='sudo ', intents=intents)

#ALLOWED_COMMANDS = ["ls", "pwd", "whoami"]  # Lista blanca de comandos permitidos


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
