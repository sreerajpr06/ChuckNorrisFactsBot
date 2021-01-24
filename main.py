import discord
import os
import requests


class MyClient(discord.Client):
    async def on_ready(self):
        print("Logged in as {0.user}".format(client))

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content == "$Hello":
            await message.channel.send("Hello!")

        if message.content == "$random":
            data = requests.get("https://api.chucknorris.io/jokes/random")
            data = data.json()
            await message.channel.send(data["value"])


client = MyClient()
client.run(os.getenv("TOKEN"))