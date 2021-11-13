#######################################
#
# File: coinflip_cog.py
#
# Created: Wed Oct 13 2021 18:26 PT
#
# Created by Siddharta Dutta
#
#######################################

# IMPORTS
import random
from discord.ext import commands
import Cogs_Utilities.DatabaseTools

# COINFLIP_COG CLASS
class coinflip_cog(commands.Cog):

  # CONSTRUCTOR METHOD
  def __init__(self, bot):

    # ----- private variables for mini-game ----- #

    # assigns obj to a bot (in this case the "client" obj)
    self.bot = bot
    self.id = 880339501413728316

    # trigger - allows asynch on reaction event to work
    self.COINFLIP_TRIGGER = False

    # wager variable - stores amt to be wagered (defaults to 0 in initial call cmd)
    self.wager = 0.00

    # value being guessed by player
    self.guessVal = 0

    # private string for future access
    #sentMsg = ""
    self.sentMsg = ""

  # COIN FLIP GAME
  async def runFlip(self, reaction, user, wager):
    
    # reset trigger to keep from running when not being played
    self.COINFLIP_TRIGGER = False

    # process user reaction/selection
    if str(reaction.emoji) == "☝️":
      self.guessVal = 1

    elif str(reaction.emoji) == "✌️":
      self.guessVal = 2
    
    else:
      await reaction.message.channel.send("Runtime Error: Please select one of the provided reactions.")

    # clears reactions to prevent multiple choices
    await reaction.message.clear_reactions()

    # verifies and processes wager
    runCon = await Cogs_Utilities.DatabaseTools.dbRunPlayer(user, reaction.message.channel, wager)

    if runCon:

      # win var
      win = None

      # randomizes game number
      gambNum = random.randint(0,1)

      # win off HEADS guess
      if(gambNum % 2 == 0) and (self.guessVal == 2):
        await reaction.message.channel.send("> " + user.mention + " picked HEADS - You Won!")
        globals()[win] = True

      # win off TAILS guess
      elif(gambNum % 2 == 1) and (self.guessVal == 1):
        await reaction.message.channel.send("> " + user.mention + " picked TAILS - You Won!")
        globals()[win] = True

      # lose off HEADS guess
      elif(gambNum % 2 == 1) and (self.guessVal == 2):
        await reaction.message.channel.send("> " + user.mention + " picked HEADS - You Lost!")
        globals()[win] = False

      # lose off TAILS guess
      elif(gambNum % 2 == 0) and (self.guessVal == 1):
        await reaction.message.channel.send("> " + user.mention + " picked TAILS - You Lost!")
        globals()[win] = False

      # fail safe for runtime error
      else:
        await reaction.message.channel.send("Runtime Error: COINFLIP-runFlip-L98")

      # if user wins, add back (wager * multiplier) to user balance
      if globals()[win]:
        Cogs_Utilities.DatabaseTools.dbAmend(user, wager, "ADD", 2.0)

    else:
      pass

  # DISPLAY GAME MENU
  @commands.command(name = "flip", help = "Coin flip game (default wager of 5 SC)")
  async def flip(self, ctx, arg: float = 5.00):

    # attempt to convert wager to float
    # if successful - print game choice msg and display reactions
    # if failure - print out error msg
    try:

      # attempt conversion
      self.wager = float(arg)

      # if conversion successful, print out msg & display reactions
      self.sentMsg = await ctx.channel.send('Chose 1 for TAILS or 2 for HEADS')
      await self.sentMsg.add_reaction('☝️')
      await self.sentMsg.add_reaction('✌️')

      # set trigger to "True" to allow reaction detection to work properly
      self.COINFLIP_TRIGGER = True
      
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
        if self.COINFLIP_TRIGGER:

          # runs game
          await self.runFlip(reaction, user, self.wager)