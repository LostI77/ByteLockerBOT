## Documentación de ByteLocker

### Introducción
ByteLocker es un bot de Discord diseñado para moderar, realizar encuestas de conocimientos en ciberseguridad, tocar música, publicar noticias, y proporcionar herramientas de escaneo de IP y URL a través de VirusTotal.

### Dependencias
- `dotenv`
- `discord`
- `discord.ext`
- `json`
- `os`
- `yt_dlp`
- `aiohttp`
- `asyncio`
- `random`

### Variables de Entorno
El bot utiliza variables de entorno que deben estar definidas en un archivo `.env`:
- `DISCORD_TOKEN`: Token del bot de Discord.
- `NEWS_CHANNEL_ID`: ID del canal donde se publicarán noticias.
- `REVIEW_CHANNEL_ID`: ID del canal donde se revisarán las respuestas de las encuestas.
- `VERIFIED_ROLE`: ID del rol que se asignará a los usuarios que aprueben la encuesta.
- `VIRUSTOTAL_TOKEN`: Token de API de VirusTotal.

### Funcionalidades Principales

#### 1. Palabras Prohibidas (BLACKLIST)
El bot eliminará mensajes que contengan palabras o enlaces especificados en la lista `BLACKLIST`.

#### 2. Encuestas de Ciberseguridad
El bot tiene un conjunto de preguntas de ciberseguridad categorizadas en tres niveles de dificultad: fáciles, medias y difíciles.

##### Comando `-preguntas`
Muestra todas las preguntas de la encuesta.

##### Comando `-encuesta`
Inicia una encuesta para el usuario que ejecuta el comando. Opcionalmente, el comando puede aceptar un modo "dev" para asignar directamente el rol verificado.

```python
@bot.command(name='encuesta')
async def start_survey(ctx, modo: str = None):
```

#### 3. Publicación de Noticias (Comentado)
Esta sección, actualmente comentada, permite al bot publicar noticias cada hora en un canal especificado.

#### 4. Logs de Mensajes

##### Comando `-logs`
Permite a los usuarios con el rol "Co-founder" listar y guardar los logs de mensajes en un canal específico.

```python
@bot.command()
@commands.has_role("Co-founder")
async def logs(ctx, action, channel_name=None):
```

#### 5. Reproducción de Música (WIP)

##### Comando `-play`
Reproduce música desde una URL de YouTube en el canal de voz del usuario.

```python
@bot.command()
async def play(ctx, url):
```

##### Comando `-skip`
Detiene la reproducción actual y salta a la siguiente canción.

```python
@bot.command()
async def skip(ctx):
```

#### 6. Escaneo de IP y URL con VirusTotal

##### Comando `-scanip`
Escanea una IP utilizando la API de VirusTotal y devuelve la puntuación de análisis.

```python
@bot.command()
async def scanip(ctx, ip):
```

##### Comando `-scanurl`
Escanea una URL utilizando la API de VirusTotal.

```python
@bot.command()
async def scanurl(ctx, url):
```

##### Comando `-scanfile`
Escanea un archivo adjunto utilizando la API de VirusTotal.

```python
@bot.command()
async def scanfile(ctx):
```

#### 7. Moderación de Mensajes

El bot registra todos los mensajes en un log y los marca como eliminados si contienen palabras de la `BLACKLIST`.

```python
@bot.event
async def on_message(message):
```

### Eventos del Bot

#### `on_ready`
Se ejecuta cuando el bot se conecta correctamente.

```python
@bot.event
async def on_ready():
```

#### `on_message`
Se ejecuta cada vez que se envía un mensaje en cualquier canal donde el bot tenga permisos.

```python
@bot.event
async def on_message(message):
```

#### `on_message_delete`
Marca un mensaje como eliminado en los logs.

```python
@bot.event
async def on_message_delete(message):
```

### Comandos de Administración

##### Comando `-nuke`
Elimina todos los mensajes de un canal. Solo puede ser ejecutado por usuarios con el rol "Co-founder".

```python
@bot.command()
@commands.has_role("Co-founder")
async def nuke(ctx):
```

### Ejecución del Bot
Para ejecutar el bot, asegúrate de tener todas las dependencias instaladas y el archivo `.env` correctamente configurado. Luego, ejecuta el script:

```python
python ByteLocker.py
```

### Conclusión
ByteLocker es un bot versátil que proporciona diversas funcionalidades útiles para la moderación, educación y entretenimiento en servidores de Discord, con un enfoque en la ciberseguridad.