#######################################
#
# File: usercmds_cog.py
#
# Created: Fri Oct 22 2021 18:26 PT
#
# Created by Siddharta Dutta
#
#######################################

# IMPORTS
from discord.ext import commands
import Cogs_Utilities.DatabaseTools

class usercmds_cog(commands.Cog):

  # CONSTRUCTOR METHOD
  def __init__(self, bot):

    # ----- private variables for mini-game ----- #

    # assigns obj to a bot (in this case the "client" obj)
    self.bot = bot

  @commands.command(name = "balance", help = "Outputs your current balance in SC")
  async def balance(self, ctx):
    await ctx.channel.send("Your balance is: " + str( Cogs_Utilities.DatabaseTools.dbSearch_JSON(ctx.message.author, "BAL")) + " SC")

  @commands.command
  async def bal(self, ctx):
    pass    