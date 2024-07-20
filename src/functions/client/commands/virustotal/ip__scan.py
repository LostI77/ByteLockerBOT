import discord
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp
import os

load_dotenv()  # Cargar variables del archivo .env

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='sudo ', intents=intents)
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

bot.run(os.getenv('DISCORD_TOKEN'))
