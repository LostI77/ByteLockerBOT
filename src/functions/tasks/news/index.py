from discord.ext import tasks
import os
import aiohttp
import asyncio


# -------------------------------------------------------------------------------
#region Noticias (Comentado)


@tasks.loop(hours=1)  # Se ejecuta cada hora, ajusta la frecuencia según tus necesidades
async def publish_news(bot):
    news_channel_id = int(os.getenv('NEWS_CHANNEL_ID'))  # Convertir a entero
    async with aiohttp.ClientSession() as session:
        async with session.get('https://hacker-news.firebaseio.com/v0/topstories.json') as resp:
            top_stories = await resp.json()
        # Tomamos las 5 noticias más importantes
        for story_id in top_stories[:5]:
            async with session.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json') as resp:
                story = await resp.json()
            # Verificamos si la noticia tiene título y URL
            if 'title' in story and 'url' in story:
                canal = bot.get_channel(news_channel_id)
                if canal is not None:
                    mensaje = f"**{story['title']}**\n{story['url']}"
                    await canal.send(mensaje)
                    await asyncio.sleep(1)  # Pequeña pausa para evitar sobrecargar la API
                else:
                    print(f"Error: No se encontró el canal con ID {news_channel_id}")
@publish_news.after_loop
async def after_publish_news():
    print("「🗞」Hacker-News - published completed")
# -------------------------------------------------------------------------------
