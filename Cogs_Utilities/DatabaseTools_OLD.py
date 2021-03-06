#######################################
#
# File: DatabaseTools_OLD.py
#
# Created: Fri Nov 13 2021 18:26 PT
#
# Created by Siddharta Dutta
#
#######################################

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