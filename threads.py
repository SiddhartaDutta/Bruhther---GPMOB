#######################################
#
# File: misc_cog.py
#
# Created: Wed Oct 27 2021 18:11 PT
#
# Created by Siddharta Dutta
#
#######################################

# IMPORTS
import discord
from discord.ext import commands
import time
from datetime import datetime
import threading
from discord.ext import tasks

"""
# THREADS_COG CLASS
class threads_cog(commands.Cog):

  # CONSTRUCTOR METHOD
  def __init__(self, bot):

    # ----- private variables for mini-game ----- #

    # assigns obj to a bot (in this case the "client" obj)
    self.bot = bot

    self.spt = None
    self.setPresence.start()

  #@tasks.loop(seconds=1)
  async def setPresence(self):

    dayOfTheWeek = ["Monday", "Turnt Tuesday", "Wooback Wednesday", "Dababy Dursday", "Freaky Friday", "Sigma Saturday", "Sugma Sunday"]

    #while True:

    currentDay = datetime.today().weekday()

    await self.bot.change_presence(activity = discord.Activity(name = dayOfTheWeek[currentDay], type = 5))

    #self.spt = threading.Thread(name = 'setPresence', target = setPresence, args = (self,))
  #setPresenceThread.start()

  def activate(self):
    self.spt = threading.Thread(name = 'setPresence', target = setPresence, args = (self,))
"""

# BOT PRESENCE
# *************************************************************** #

async def setPresence(bot):

  dayOfTheWeek = ["Money Monday", "Turnt Tuesday", "Wooback Wednesday", "Dababy Dursday", "Freaky Friday", "Sigma Saturday", "Sugma Sunday"]

  #while True:

  currentDay = datetime.today().weekday()

  await bot.change_presence(activity = discord.Activity(name = dayOfTheWeek[currentDay], type = 5))