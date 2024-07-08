# Bot de Discord

## Introducción
Este bot de Discord está diseñado para realizar diversas funciones, incluyendo la moderación de mensajes, reproducción de música desde YouTube, y escaneo de URLs y archivos usando la API de VirusTotal.

## Requisitos
- Python 3.6 o superior
- Discord.py
- yt-dlp (para la reproducción de música)
- aiohttp (para las solicitudes HTTP)
- ffmpeg (para la reproducción de audio)
- Una cuenta en VirusTotal y su clave de API

## Instalación
1. **Clonar el repositorio o descargar el código fuente:**
   ```bash
   git clone <repositorio_url>
   cd <repositorio>
   ```
2. **Crear un entorno virtual y activarlo:**

```bash
python -m venv venv
source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
```
3. **Instalar las dependencias:**

```bash
pip install -r requirements.txt
```

## Configuración
1. **Configurar las variables de entorno:**

- Crea un archivo .env en la raíz del proyecto y agrega las siguientes variables:
```bash
DISCORD_TOKEN=tu_token_de_discord
VIRUSTOTAL_TOKEN=tu_token_de_virustotal
```
## Uso
1. **Iniciar el bot:**

```bash
python ByteLocker.py
```
## Comandos disponibles:
```bash
-play <url>: Reproduce música desde una URL de YouTube.
-skip: Salta la canción actual.
-scanurl <url>: Escanea una URL usando la API de VirusTotal.
-scanfile: Escanea un archivo adjunto usando la API de VirusTotal.
-logs dump <channel_name>: Guarda los registros de mensajes de un canal en un archivo JSON.
-logs list channels: Lista los canales registrados.
```