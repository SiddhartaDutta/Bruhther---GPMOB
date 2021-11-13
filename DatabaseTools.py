#######################################
#
# File: DatabaseTools.py
#
# Created: Sat Sep 18 2021 17:29 PT
#
# Created by Siddharta Dutta
#
#######################################

import json

def dbSearch_JSON(user, channel, returnType):

  # int for "LOC" return option
  loc = 0

  # memory cache user data Json object file
  with open('userDatabase.json', 'r') as tempDBAccess:

    tempJsonObj = json.load(tempDBAccess)

    # scan through Json tree looking for matching user id
    for num in range(len(tempJsonObj)):

      # update location
      loc = num

      # if user id found, return requested data
      if(tempJsonObj['userData'][num]['id'] == user.id):

        # return based on requested data type
          # return boolean
        if returnType == "BOOL":
          return True

          # return location in Json tree (float)
        elif returnType == "FLOAT":
          return float(loc)

          # return balance (float)
        elif returnType == "BAL":
          return float(tempJsonObj['userData'][num]['balance'])
          
  # return that user was not found
    # return boolean
  if returnType == "BOOL":
    return False

    # return float
  else:
    return float(0)
    #await channel.send("Runtime Error: DBTOOLS-dbSearch-L51")


# Searches for user id - Returns "True" if found, "False" if not
def dbSearch(user, channel, returnType):

  # int for "int" return option
  loc = 0

  # memory cache user data into list
  with open("UserIDs.txt", "r") as tempFileAccess_ID:
    idData = list(tempFileAccess_ID)

    # scan thru file looking for matching user id num
    for w in range(len(idData)):

      # update loc
      loc = w

      # temp string for adjusting ID declaration
      tempStr = ""

      # read into temp string removing extra space from new line
        # 18 - default id size
      for c in range(18):
        tempStr += str(idData[w][c])

      # if user found, close file, stop search, return "True"
      if tempStr == str(user.id):

        # return based on type
          # return "True" that user exists in DB
        if returnType == "BOOL":
          return True
        
          #return location of user/corresponding balance
        elif returnType == "INT":
          return int(loc)

          # return user balance
        elif returnType == "BAL":
          
          # find balance from loc and return
          with open("Balances.txt", "r") as tempFileAccess_BAL:
            balData = list(tempFileAccess_BAL)
            return float(balData[loc])

  # return based on type
  if returnType == "BOOL":
    return False
  elif returnType == "INT":
    return int(loc)
  else:
    pass
    #await channel.send("Runtime Error: DBTOOLS-dbSearch-L51")

# Write new user data to Json database
def dbWrite_JSON(user, balance):

  # create temporary Python object
  newUser = {
              'id': user.id,
              'balance': float(100)
  }

  # memory cache user data Json object file
  with open('userDatabase.json', 'a') as tempDBAccess:

    # create a temporary Json object from Json in DBFILE
    tempJsonObj = json.load(tempDBAccess)

    # append temp Json object
    tempJsonObj['userData'].append(newUser)

    # load Json object into DBFILE
    json.dump(tempJsonObj, tempDBAccess, indent = 2)

# Write new to databases
def dbWrite(user, balance):

  with open("UserIDs.txt", "a") as tempFileAccess_ID:
    # write to id
    tempFileAccess_ID.write("\n" + str(user.id))

  with open("Balances.txt", "a") as tempFileAccess_BAL:
    # write to bal
    tempFileAccess_BAL.write(" \n" + str(balance))

# amend bal info based on user "location"
def dbAmend(user, wager, operation, multiplier):

  # locate user on file
  loc = dbSearch(user, None, "INT")

  if operation == "ADD":

    # memory cache balance data into list and adjust user balance
    with open("Balances.txt", "r") as tempFileAccess_BAL:
      balData = list(tempFileAccess_BAL)
      balData[loc] = float( float(balData[loc]) + (multiplier * wager) )

  else:

    # memory cache balance data into list and adjust user balance
    with open("Balances.txt", "r") as tempFileAccess_BAL:
      balData = list(tempFileAccess_BAL)
      balData[loc] = float( float(balData[loc]) - wager )

  # amend strings and rewrite into file
  with open("Balances.txt", "w") as tempFileAccess_BAL:

    # increment through values
    for w in range(len(balData)):

      tempStr = ""

      # increment through characters (or integers)
      for c in str(balData[w]):
        
        # write only to tempStr when char not ' ' - when "space" break from loop to iterate next word
        if c != ' ':
          tempStr += c
        else:
          break
      
      # make make word being amended tempStr - rids of " \n"
      balData[w] = tempStr

    # increment through adjusted list to write into file
    for x in range(len(balData)):

      # if 1st data point, do not add shift down a line
      if x == 0:
        tempFileAccess_BAL.write(str(balData[0]))
      else:
        tempFileAccess_BAL.write(" \n" + str(balData[x]))

# process wager
def dbProcessWager(user, channel, wager):

  # if wager too high, return false
  if (dbSearch(user, None, "BAL") - wager) < 0:
    return False
  else:
    return True

# *************************************************************** #

# runs player-wager routine
async def dbRunPlayer(user, channel, wager):

  # check if player does NOT exist
  if dbSearch(user, None, "BOOL") != True:
    dbWrite(user, 100)

  # if player exists, check if wager is too high, if not, amend balance, return "True" to run game
  if dbProcessWager(user, channel, wager) == True:
    dbAmend(user, wager, None, None)
    return True
  
  elif dbProcessWager(user, channel, wager) == False:
    await channel.send("Request Error: Insufficient Funds")
    return False

  # fail safe to pause game
  else:
    await channel.send("Runtime Error: DBTOOLS-dbRunPlayer-L143\n\tPlease message Iyes#8866")
    return False