import discord
from discord.ext import commands
import os

from functions.client.commands.virustotal.domain__scan import scanurl
from functions.client.commands.virustotal.file__scan import scanfile
from functions.client.commands.virustotal.ip__scan import scanip
from functions.client.commands.passwd.index import passwd
from functions.client.commands.whome.index import whome
from functions.client.commands.reboot.index import reboot
from functions.admin.commands.surveys.index import conduct_survey, start_survey
from functions.admin.commands.nuke.index import nuke

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='sudo ', intents=intents)

commandsList = [scanurl, scanfile, scanip, passwd, whome, reboot, conduct_survey, start_survey, nuke]

async def setup():
    for c in commandsList:
        bot.add_command(c)
        print(bot.commands)

bot.run(os.getenv('DISCORD_TOKEN'))