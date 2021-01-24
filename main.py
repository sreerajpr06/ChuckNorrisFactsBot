import discord
import os
import requests
from decouple import config

client = discord.Client()
categories = []

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))
    data = requests.get("https://api.chucknorris.io/jokes/categories")
    data = data.json()

    global categories
    categories = data


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "$random":
        data = requests.get("https://api.chucknorris.io/jokes/random")
        data = data.json()
        await message.channel.send(data["value"])

    if message.content == "$showCategories":
        data = '\n'.join(categories)
        await message.channel.send(data)

    if message.content[1:] in categories and message.content[0] == "$":
        category = message.content[1:]
        url = "https://api.chucknorris.io/jokes/random?category=" + category
        data = requests.get(url)
        data = data.json()
        data = data["value"]
        await message.channel.send(data)


TOKEN = config("TOKEN")
client.run(TOKEN)