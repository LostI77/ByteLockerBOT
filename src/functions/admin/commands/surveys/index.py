import discord
from discord.ext import commands
from constants.questions import questions
from dotenv import load_dotenv
import asyncio
import random
import os

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='sudo ', intents=intents)
#region Encuesta
@commands.command(name='conduct_survey')
async def conduct_survey(member, channel):
    total_score = 0
    responses = []
    def check(m):
        return m.author == member and m.channel == channel and m.content.isdigit() and 1 <= int(m.content) <= 4
    # Selecciona 5 preguntas al azar
    selected_questions = random.sample(list(questions.items()), k=5)
    for question, (correct_answer, points) in selected_questions:
        await channel.send(question)
        try:
            msg = await bot.wait_for('message', check=check, timeout=60)
            try:
                user_answer = int(msg.content)
                responses.append((question, user_answer))
                if user_answer == correct_answer:
                    total_score += points
            except ValueError:
                await channel.send(f'{member.mention}, por favor introduce un número válido entre 1 y 4.')
        except asyncio.TimeoutError:
            await channel.send(f'{member.mention}, no respondiste a tiempo. Intenta nuevamente.')
            return


    # Envía las respuestas
    review_channel = bot.get_channel(int(os.getenv('REVIEW_CHANNEL_ID')))
    print(f"review_channel: {review_channel}")
    if review_channel:
        response_str = "\n".join([f"{q}: {r}" for q, r in responses])
        await review_channel.send(f'Respuestas de {member.mention}:\n{response_str}')

    # Asigna rol si aprobó
    if total_score >= 75:
        await channel.send(f'{member.mention}, ¡felicitaciones! Has pasado la encuesta con {total_score} puntos.')
        # Asigna rol
        role_id = int(os.getenv('VERIFIED_ROLE'))
        print(f"role_id: {role_id}")
        role = channel.guild.get_role(role_id)
        if role:
            await member.add_roles(role)
            await channel.send(f'Te he asignado el rol {role.name}.')
        else:
            await channel.send('No se pudo encontrar el rol especificado.')
        await channel.send(f'{member.mention}, tus respuestas están siendo revisadas por un administrador. Obtuviste {total_score} puntos.')

# @bot.event
# async def on_member_join(member):
#     welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)
#     if welcome_channel is not None:
#         await welcome_channel.send(f'¡Bienvenido {member.mention}! Responde las siguientes preguntas:')
#         await conduct_survey(member, welcome_channel)
#region Iniciar Encuesta

@commands.command(name='start_survey')
async def start_survey(ctx):
    print("Encuesta command triggered!")
    await ctx.send(f'{ctx.author.mention}, iniciaré la encuesta contigo.')
    print(f"Comando encuesta iniciado por {ctx.author}")
    await conduct_survey(ctx.author, ctx.channel)

# -------------------------------------------------------------------------------

bot.run(os.getenv('DISCORD_TOKEN'))