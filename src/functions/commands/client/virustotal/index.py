from discord.ext import commands
from dotenv import load_dotenv
import aiohttp
import json
import os

load_dotenv()  # Cargar variables del archivo .env


class VirusTotal(commands.Cog):
    @commands.command()
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
    @commands.command()
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
    @commands.command()
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

async def setup(bot):
    await bot.add_cog(VirusTotal)