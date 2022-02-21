import os
import discord
import random
import datetime
from dotenv import load_dotenv
import mysql.connector as mysql

################ LOADING ENVIRONMENT VARIABLES #################
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
MYSQLHOST = os.getenv('MYSQLHOST')
MYSQLUSER = os.getenv('MYSQLUSER')
MYSQLPASSW = os.getenv('MYSQLPASSW')
MYSQLDB = os.getenv('MYSQLDB')

################ CONNECTING TO DATABASE #################
mydb = mysql.connect(
    host=MYSQLHOST,
    user=MYSQLUSER,
    password=MYSQLPASSW,
    database=MYSQLDB
)
mycursor = mydb.cursor()

################ DISCORD EVENTS ######################
client = discord.Client()

@client.event
async def on_ready():
  print(f'{client.user} is online and ready to roll!')

@client.event
async def on_message(message):
  if(message.author == client.user):
    return

  msg = message.content

  if(msg.startswith(';pokemon')):
    if(checkLastPokeGet(message.created_at, message.author)):
      embedObj = newPokemonMessage(message.author)
      await message.channel.send(embed=embedObj)
    else:
      await message.channel.send("Please wait 1 hour from your last Pokemon for a new one! :purple_heart:")
    
  if(msg.startswith(';inv')):
    embedObj = getUsersPokemon(message.author)
    await message.channel.send(embed=embedObj)

  if(msg.startswith(';help')):
    await message.channel.send("You may either chose to catch a new pokemon with: \n     **;pokemon** \nOr you can check what pokemon you already have with: \n     **;inv**")

#####################   GET USERS ID FROM DATABASE #########################

def getUserId(data):
  getUserData = "SELECT * FROM users WHERE username = '"+str(data)+"'"
  mycursor.execute(getUserData)
  userData = mycursor.fetchall()
  cleanUserId = userData[0]
  return cleanUserId

#####################  THESE FUNCTIONS DEAL WITH GETTING A NEW POKEMON USING ;POKEMON ########################

def checkLastPokeGet(date, user):
  userId = getUserId(user)[0]
  query = "SELECT captureDate FROM uniquePokemon WHERE userId='"+str(userId)+"'"
  mycursor.execute(query)
  dirtyData = mycursor.fetchall()
  if not dirtyData:
    return True

  cleanData = dirtyData[-1][0]
  threeHourLater = cleanData + datetime.timedelta(hours=1)
  current = datetime.datetime.now()
  if current > threeHourLater:
    return True
  else:
    return False

def newPokemonMessage(data):
  newPoke = getNewPokemon()
  addUserPoke(data, newPoke)
  message = makeEmbeddedMessage(newPoke)
  return message

def getNewPokemon():
  ranNum = random.randint(1,151)
  query = "SELECT * FROM pokemon WHERE id = "+str(ranNum)
  mycursor.execute(query)
  result = mycursor.fetchall()
  return result[0]

def addUserPoke(userName, pokemonData):
  pokeId = pokemonData[0]
  userId = getUserId(userName)[0]

  insertUserPokemon = "INSERT INTO uniquePokemon (userId, pokeId) values ("+str(userId)+", "+str(pokeId)+")"
  mycursor.execute(insertUserPokemon)
  mydb.commit()
  return None

def makeEmbeddedMessage(newPoke):
  pokeName = newPoke[1]
  pokeImage = newPoke[3]
  embedMessage = discord.Embed(
    title="New Pokemon Catch!",
    description="New Pokemon "+str(pokeName)+" was caught!",
    color=discord.Color.blue(),
  )
  embedMessage.set_image(url=pokeImage)
  #embedMessage.set_thumbnail(url='https://www.freeiconspng.com/thumbs/pokeball-png/pokeball-transparent-png-2.png')
  return embedMessage

############################## THESE FUNCTIONS DEAL WITH ;INV COMMAND ##############################

def getUsersPokemon(data):
  userId = getUserId(data)[0]

  fetchUsersPokemon = "SELECT * FROM uniquePokemon LEFT JOIN pokemon ON uniquePokemon.pokeId=pokemon.id AND uniquePokemon.userId='"+str(userId)+"'"
  mycursor.execute(fetchUsersPokemon)
  pokeData = mycursor.fetchall()

  embedMessage = discord.Embed(
    title="Your Pokemon!",
  )
  for x in pokeData:
    num = numPokeUserHas(x)
    embedMessage.add_field(name="Pokemon Captured: ", value=str(x[5])+" x"+str(num), inline=False)
  
  return embedMessage

def numPokeUserHas(data):
  query = "SELECT COUNT(*) FROM uniquePokemon WHERE userId = '"+str(data[1])+"' AND pokeId = '"+str(data[2])+"'"
  mycursor.execute(query)
  dirtyResult = mycursor.fetchall()
  cleanResult = dirtyResult[0][0]
  return cleanResult

############## CLIENT RUN ##################
client.run(TOKEN)