### Documentación del Bot de Discord

El bot ByteLocker está desarrollado en Python utilizando la biblioteca `discord.py` y ofrece diversas funcionalidades como moderación de mensajes, encuestas, logging de mensajes y más. A continuación se detallan las características y el uso del bot.

#### Requisitos

- Python 3.6+
- Discord.py
- Youtube-dl (yt_dlp)
- aiohttp
- dotenv

#### Instalación

1. Clona el repositorio o descarga el código fuente.
2. Crea un archivo `.env` en el mismo directorio con el siguiente contenido:
   ```env
   DISCORD_TOKEN=your_discord_token
   VIRUSTOTAL_TOKEN=your_virustotal_api_key
   ```
3. Instala las dependencias:
   ```sh
   pip install discord.py yt-dlp aiohttp python-dotenv
   ```

#### Funcionalidades

##### 1. Moderación de Mensajes

El bot elimina mensajes que contengan palabras malsonantes o enlaces de spam definidos en la lista negra.

```python
BLACKLIST = ["badword1", "badword2", "spamlink.com"] (Está en Desarrollo)
```

##### 2. Encuestas

El bot realiza una encuesta a los usuarios con preguntas predefinidas. Dependiendo de las respuestas, se asigna un puntaje y, si es suficiente, se otorga un rol al usuario.

```python
questions = {
    "¿Pregunta 1?\n1. Lorem ipsum\n2. Dolor sit amet\n3. Consectetur\n4. Adipiscing elit": (2, 20),
    "¿Pregunta 2?\n1. Sed do eiusmod\n2. Tempor incididunt\n3. Ut labore et dolore\n4. Magna aliqua": (2, 30),
    "¿Pregunta 3?\n1. Ut enim ad minim\n2. Veniam, quis nostrud\n3. Exercitation ullamco\n4. Laboris nisi": (2, 25),
} (Preguntas en desarrollo)
```

###### Comando

- `-encuesta`: Inicia la encuesta para el usuario que ejecuta el comando.

##### 3. Logging de Mensajes

El bot almacena mensajes y puede listar los canales con logs y guardar los logs de un canal específico en un archivo JSON.

###### Comandos

- `-logs dump <channel_name>`: Guarda los logs del canal especificado en un archivo JSON.
- `-logs list channels`: Lista los canales que tienen logs almacenados.

##### 4. Reproducción de Música

**Nota: Esta funcionalidad no está completamente funcional y puede requerir ajustes adicionales.**

El bot puede unirse a un canal de voz y reproducir música desde YouTube.

###### Comandos

- `-play <url>`: Reproduce música desde la URL de YouTube proporcionada.
- `-skip`: Salta la canción actual.

##### 5. Escaneo de URLs y Archivos

El bot puede escanear URLs y archivos adjuntos utilizando la API de VirusTotal. **Nota: Esta funcionalidad está en proceso y puede requerir ajustes adicionales.**

###### Comandos

- `-scanurl <url>`: Escanea la URL proporcionada utilizando VirusTotal.
- `-scanfile`: Escanea el archivo adjunto utilizando VirusTotal.

##### 6. Comando Ping

El bot responde con "pong" para verificar que está funcionando correctamente.

###### Comando

- `-ping`: Responde con "pong".

#### Ejemplo de Uso

```sh
# Correr el bot
python bot.py
```

En Discord, puedes usar los siguientes comandos:

- `-ping`: Verifica el funcionamiento del bot.
- `-encuesta`: Inicia la encuesta.
- `-logs dump <channel_name>`: Guarda los logs del canal especificado.
- `-logs list channels`: Lista los canales con logs.
- `-play <url>`: (No funcional) Reproduce música desde la URL.
- `-skip`: (No funcional) Salta la canción actual.
- `-scanurl <url>`: Escanea la URL.
- `-scanfile`: Escanea el archivo adjunto.

### Notas

- Asegúrate de configurar correctamente los permisos del bot en Discord para que pueda leer y escribir mensajes, gestionar roles, y unirse a canales de voz.
- Algunas funcionalidades, como la reproducción de música y el escaneo de URLs/archivos, pueden requerir ajustes adicionales y no están completamente funcionales en esta versión.
