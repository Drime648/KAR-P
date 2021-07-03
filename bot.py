import discord
import os
import random
from keep_alive import keep_alive
import pandas as pd
import requests
import json

targets = pd.read_csv("https://raw.githubusercontent.com/t-davidson/hate-speech-and-offensive-language/master/lexicons/refined_ngram_dict.csv")
targets = targets.drop("prophate", axis = 1)
targets = targets["ngram"]


url = "https://cnnhackathon.herokuapp.com/predict/?text="




client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person!"
]




@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  

  



  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))

  if any(word in msg for word in targets):

    response = requests.get(url + msg)
    json_data = json.loads(response.text)

    answer = json_data["VERDICT"]

    if(answer != "clean"):
      await message.delete()
      string = f"you have been kicked out because of your use of {answer} in a zero tolerance server. You sent a message saying '{msg}'. If you feel this is unfair, please send a message to a moderator from the server with a screenshot of this text."
      await message.author.send(string)
      await message.channel.send(message.author.name + " has been kicked")
      await message.author.kick(reason = answer)


      



 

keep_alive()
client.run(os.getenv('TOKEN'))