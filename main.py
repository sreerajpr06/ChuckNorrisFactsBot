import discord
import os
import requests


client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "$random":
        data = requests.get("https://api.chucknorris.io/jokes/random")
        data = data.json()
        await message.channel.send(data["value"])

    if message.content == "$showCategories":
        data = requests.get("https://api.chucknorris.io/jokes/categories")
        data = data.json()
        data = '\n'.join(data)
        await message.channel.send(data)

client.run(os.getenv("TOKEN"))