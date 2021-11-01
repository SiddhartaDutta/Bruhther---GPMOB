#######################################
#
# File: main.py
#
# Created: Wed Aug 25 2021 23:46 PT
#
# Created by Siddharta Dutta
#
#######################################

# IMPORTS
import os
import discord
from discord.ext import commands
from Cogs.usercmds_cog import usercmds_cog
import asyncio

# BOT COGS
#from usercmds_cog import usercmds_cog
from music_cog import music_cog
from coinflip_cog import coinflip_cog
from crash_cog import crash_cog

# BOT THREADS
from threads import setPresence

# SET COMMAND PREFIX
Bruhther_Bot = commands.Bot(command_prefix = "$", description = "TEST DESC")

# INITIALIZE
# *************************************************************** #

  # connect to discord servers
@Bruhther_Bot.event
async def on_connect():
    print('Client: Successfully connected to Discord')

  # log into discord
@Bruhther_Bot.event
async def on_ready():
    print('Client: Logged in as -> {0.user}'.format(Bruhther_Bot))
    #await activateThreads(Bruhther_Bot,)
    await asyncio.sleep(10)
    await setPresence(Bruhther_Bot)

# ATTACH COGS
# *************************************************************** #

Bruhther_Bot.add_cog(usercmds_cog(Bruhther_Bot))
Bruhther_Bot.add_cog(music_cog(Bruhther_Bot))
Bruhther_Bot.add_cog(coinflip_cog(Bruhther_Bot))
Bruhther_Bot.add_cog(crash_cog(Bruhther_Bot))
#Bruhther_Bot.add_cog(threads_cog(Bruhther_Bot))

#Bruhther_Bot.add_cog(thread_cog(Bruhther_Bot))

# *************************************************************** #

# ACTIVATE THREADS
# *************************************************************** #

# *************************************************************** #

Bruhther_Bot.run(os.getenv('testkey'))