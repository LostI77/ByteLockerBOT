import discord
from discord.ext import commands
from dotenv import load_dotenv
import yt_dlp as youtube_dl

load_dotenv()  # Cargar variables del archivo .env

class Music(commands.Cog):
    #region Música (WIP)
    @commands.command()
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

    @commands.command()
    async def skip(ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.send("Canción saltada.")
        else:
            await ctx.send("No hay ninguna canción en reproducción.")

async def setup(bot):
    await bot.add_cog(Music(bot))