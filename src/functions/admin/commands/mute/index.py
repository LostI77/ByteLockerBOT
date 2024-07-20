import discord
from discord.ext import commands
from dotenv import load_dotenv
import os


load_dotenv()  # Cargar variables del archivo .env

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='sudo ', intents=intents)

#region Mute
@bot.command(name="mute")
@commands.has_role('Co-founder')
@commands.has_permissions(manage_roles=True) # Requiere permiso para gestionar roles
async def mute(ctx, member: discord.Member, *, reason=None):
    # ID del rol a quitar (reemplázalo con el ID correcto)
    rol_a_quitar_id = int(os.getenv('VERIFIED_ROLE'))

    # ID del rol a asignar (reemplázalo con el ID correcto)
    rol_a_asignar_id =  int(os.getenv('MUTED_ROLE_ID'))

    rol_a_quitar = ctx.guild.get_role(rol_a_quitar_id)
    rol_a_asignar = ctx.guild.get_role(rol_a_asignar_id)
    if rol_a_quitar and rol_a_asignar:
        await member.remove_roles(rol_a_quitar, reason=reason)
        await member.add_roles(rol_a_asignar, reason=reason)
        await ctx.send(f"{member.mention} ha sido silenciado.")
    else:
        await ctx.send("Error: No se encontraron los roles especificados.")

# -------------------------------------------------------------------------------
@bot.command(name="unmute")
@commands.has_role('Co-founder')
@commands.has_permissions(manage_roles=True) # Requiere permiso para gestionar roles
async def unmute(ctx, member: discord.Member, *, reason=None):
    # ID del rol a quitar (el que se asignó al mutear)
    rol_a_quitar_id = int(os.getenv('MUTED_ROLE_ID'))

    # ID del rol a asignar (el que se quitó al mutear)
    rol_a_asignar_id = int(os.getenv('VERIFIED_ROLE'))
    rol_a_quitar = ctx.guild.get_role(rol_a_quitar_id)
    rol_a_asignar = ctx.guild.get_role(rol_a_asignar_id)
    if rol_a_quitar and rol_a_asignar:
        await member.remove_roles(rol_a_quitar, reason=reason)
        await member.add_roles(rol_a_asignar, reason=reason)
        await ctx.send(f"{member.mention} ha sido desmuteado.")
    else:
        await ctx.send("Error: No se encontraron los roles especificados.")

@mute.error
async def logs_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("No tienes permiso para usar este comando.")
@unmute.error
async def logs_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("No tienes permiso para usar este comando.")

bot.run(os.getenv('DISCORD_TOKEN'))