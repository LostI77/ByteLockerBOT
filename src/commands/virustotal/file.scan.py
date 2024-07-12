from ByteLocker import bot
import os
import aiohttp
import json


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