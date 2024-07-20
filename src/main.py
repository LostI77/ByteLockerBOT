from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
import os
import subprocess

load_dotenv()  # Cargar variables del archivo .env

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='sudo ', intents=intents)


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
    channel = bot.get_channel(news_channel_id)
    if channel is not None:
        print(f"Canal de noticias encontrado: {channel.name}")
       # publicar_noticias.start()
    else:
        print(f"Error: No se encontró el canal con ID {news_channel_id}")
    # Importar después de la inicialización para evitar importación circular

if __name__ == "__main__":
    from setup import setup
    setup()
    bot.run(os.getenv('DISCORD_TOKEN'))
