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

    if message.content.split()[0] == "$random":
        if(len(message.content.split()) == 1):
            data = requests.get("https://api.chucknorris.io/jokes/random")
            data = data.json()
            await message.channel.send(data["value"])
        elif (len(message.content.split()) == 2 and message.content.split()[1] == "--help"):
            txt = "```" +\
                ("$random".ljust(20)) + "Shows a random fact\n\n" + \
                "For getting a random fact, type \n$random" + \
                "```"
            await message.channel.send(txt)

    if message.content.split()[0] == "$categories":
        if(len(message.content.split()) == 1):
            data = '\n'.join(categories)
            await message.channel.send(data)

        elif (len(message.content.split()) == 2 and message.content.split()[1] == "--help"):
            txt = "```" +\
                ("$categories".ljust(20)) + "Shows all available categories\n\n" + \
                "For getting all available categories, type \n$categories" + \
                "```"
            await message.channel.send(txt)

    if message.content.split()[0][1:] in categories and message.content.split()[0][0] == "$":
        if(len(message.content.split()) == 1):
            category = message.content[1:]
            url = "https://api.chucknorris.io/jokes/random?category=" + category
            data = requests.get(url)
            data = data.json()
            data = data["value"]
            await message.channel.send(data)
        
        elif (len(message.content.split()) == 2 and message.content.split()[1] == "--help"):
            txt = "```" +\
                ("$<any category>".ljust(20)) + "Shows a random fact from the selected category\n\n" + \
                "For getting a random fact of a preferred category, type \n$<any category>" + \
                "Example:\n" + message.content.split()[0] + \
                "```"
            await message.channel.send(txt)

    if message.content == "$help":
        txt = "```" + \
            ("$random".ljust(20)) + "Shows a random fact\n" + \
            ("$categories".ljust(20)) + "Shows all available categories\n" + \
            ("$<any category>".ljust(20)) + "Shows a quote from the selected category\n\n" +\
            "For details on a specific command, type\n<$command> --help\n" + \
            "Example: $random --help" + \
            "```"
        await message.channel.send(txt)


TOKEN = config("TOKEN")
client.run(TOKEN)