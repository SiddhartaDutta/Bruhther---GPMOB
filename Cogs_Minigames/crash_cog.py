#######################################
#
# File: crash_cog.py
#
# Created: Fri Oct 29 2021 14:00 PT
#
# Created by Siddharta Dutta
#
#######################################

# IMPORTS
import random
from discord.ext import commands
import asyncio
import Cogs_Utilities.DatabaseTools

# COINFLIP_COG CLASS
class crash_cog(commands.Cog):

  # CONSTRUCTOR METHOD
  def __init__(self, bot):

    # ----- private variables for mini-game ----- #

    # assigns obj to a bot (in this case the "client" obj)
    self.bot = bot
    self.id = 880339501413728316

    self.CRASH_TRIGGER = False
    self.CRASH_RUN = False
    self.CRASH_END_TRIGGER = False

    # wager variable - stores amt to be wagered (defaults to 0 in initial call cmd)
    self.wager = 0.00

    #
    self.guessVal = 0.0

    #sentMsg = ""
    self.sentMsg = ""
    
  # CRASH GAME
  async def runCrash(self, reaction, user, wager):

    # disables trigger to ensure game isn't run again on reaction
    self.CRASH_TRIGGER = False
    self.CRASH_RUN = True

    # clears reactions to prevent multiple choices
    await reaction.message.clear_reactions()

    runMax = float(random.randint(0,200)) / 10.00

    # finalize runMax with rigged 

    currentMult = 0.00
    
    self.sentMsg = await reaction.message.channel.send("> " + "Wager: " + str(self.wager) + "\n> " + "Multiplier: " + str(currentMult))

    print(str(runMax))

    while(self.CRASH_RUN and currentMult < runMax):
      
      currentMult += 0.1
      currentMult = round(currentMult, 2)

      await self.sentMsg.edit(content = "> " + "Wager: " + str(self.wager) + "\n> " + "Multiplier: " + str(currentMult))
      
      await asyncio.sleep(0.5)

    if(self.CRASH_RUN):
      self.CRASH_RUN = False
      print("stopped")
  

  @commands.command(name = "crash", help = "Crash game (default wager of 5 SC")
  async def crash(self, ctx, arg: float = 5.0):

    # attempt to convert wager to float
    # if successful - print game choice msg and display reactions
    # if failure - print out error msg
    try:

      # attempt conversion
      self.wager = float(arg)

      # if conversion successful, print out msg & display reactions
      self.sentMsg = await ctx.channel.send('Hit STOP 🛑 when you wish to end. Hit ✅ to start.')
      await self.sentMsg.add_reaction('✅')

      # set trigger to "True" to allow reaction detection to work properly
      self.CRASH_TRIGGER = True

    except:

      # error message
      ctx.channel.send('Runtime Error: Please input numerical wager.')

  # PLAY GAME FROM REACTION
  @commands.Cog.listener()
  async def on_reaction_add(self, reaction, user):

    # checks if user is not bot itself
    if user.id != self.id:

      # checks if msg being reacted to is the correct msg
      if str(reaction.message) == str(self.sentMsg):

        # checks if game is actively being played
        if self.CRASH_TRIGGER:

          # runs game
          await self.runCrash(reaction, user, self.wager)

        if self.CRASH_RUN:

          self.CRASH_RUN = False