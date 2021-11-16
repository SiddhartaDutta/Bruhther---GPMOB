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

def dbSearch_JSON(user, returnType):

  # memory cache user data Json object file
  with open('userDatabase.json', 'r') as tempDBAccess:

    # create a temporary Json object from Json in DBFILE
    tempJsonObj = json.load(tempDBAccess)

    # counter for Json branch location / int for "LOC" return option
    loc = 0

    # traverse through Json tree
    for num in tempJsonObj['userData']:

      # if user id found, return requested data
      if(num['id'] == user.id):

        # return based on requested data type
          # return boolean
        if returnType == "BOOL":
          return True

          # return location in Json tree (float)
        elif returnType == "FLOAT":
          return float(loc)

          # return balance (float)
        elif returnType == "BAL":
          return float(num['balance'])

      # update location
      loc = loc + 1
          
  # return that user was not found
    # return boolean
  if returnType == "BOOL":
    return False

    # return float
  else:
    return float(0)
    #await channel.send("Runtime Error: DBTOOLS-dbSearch-L51")

# Write new user data to Json database
def dbWrite_JSON(user, balance):

  # create temporary Python object
  newUser = {
              'id': user.id,
              'balance': float(100)
  }

  # memory cache user data Json object file
  with open('userDatabase.json', 'r') as tempDBAccess:

    # create a temporary Json object from Json in DBFILE
    tempJsonObj = json.load(tempDBAccess)

  # memory cache user data Json object file
  with open('userDatabase.json', 'w') as tempDBAccess:

    # append temp Json object
    tempJsonObj['userData'].append(newUser)

    # load Json object into DBFILE
    json.dump(tempJsonObj, tempDBAccess, indent = 2)

# Amend bal info based on user "location" on Json tree
def dbAmend_JSON(user, wager: float, operation, multiplier: float):

  # get user location on tree
  loc = dbSearch_JSON(user, "FLOAT")
  loc = int(loc)

  # memory cache user data Json object file
  with open('userDatabase.json', 'r') as tempDBAccess:

    # create a temporary Json object from Json in DBFILE 
    tempJsonObj = json.load(tempDBAccess)

  # memory cache user data Json object file
  with open('userDatabase.json', 'w') as tempDBAccess:

    # if add operation, then add into balance
    if operation == "ADD":

      # add into balance
      tempJsonObj['userData'][loc]['balance'] = float( float(tempJsonObj['userData'][loc]['balance']) + (multiplier * wager) )
      
    else:

      # subtract wager
      tempJsonObj['userData'][loc]['balance'] = float( float(tempJsonObj['userData'][loc]['balance']) - wager )

    # load Json object into DBFILE
    json.dump(tempJsonObj, tempDBAccess, indent = 2)

# process wager
def dbProcessWager(user, channel, wager):

  # if wager too high, return false
  if (dbSearch_JSON(user, "BAL") - wager) < 0:
    return False
  else:
    return True

# *************************************************************** #

# runs player-wager routine
async def dbRunPlayer(user, channel, wager):

  # check if player does NOT exist
  if dbSearch_JSON(user, "BOOL") != True:
    dbWrite_JSON(user, 100)

  # if player exists, check if wager is too high, if not, amend balance, return "True" to run game
  if dbProcessWager(user, channel, wager) == True:
    dbAmend_JSON(user, wager, None, None)
    return True
  
  elif dbProcessWager(user, channel, wager) == False:
    await channel.send("Request Error: Insufficient Funds")
    return False

  # fail safe to pause game
  else:
    await channel.send("Runtime Error: DBTOOLS-dbRunPlayer-L143\n\tPlease message Iyes#8866")
    return False