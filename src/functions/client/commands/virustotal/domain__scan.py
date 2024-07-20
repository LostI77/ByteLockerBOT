import discord
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp
import json
import os

load_dotenv()  # Cargar variables del archivo .env

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='sudo ', intents=intents)
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

bot.run(os.getenv('DISCORD_TOKEN'))