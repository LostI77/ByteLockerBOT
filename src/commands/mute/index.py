from ByteLocker import bot
import discord
from discord.ext import commands
import os

#region Mute
@bot.command()
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

@mute.error
async def logs_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("No tienes permiso para usar este comando.")
# -------------------------------------------------------------------------------
@bot.command()
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

@unmute.error
async def logs_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("No tienes permiso para usar este comando.")