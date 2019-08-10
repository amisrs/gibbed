import discord
import asyncio
import requests

client = discord.Client()
gipped_service = "http://localhost:5000/"

with open('token.txt', 'r') as token_file:
    token = token_file.read().split('\n')[0]

@client.event
async def on_message(message):
    if message.content.startswith("!kill"):
        args = message.content.split()
        target = args[1]
        response = requests.get(gipped_service + "death/" + target)
        death = response.json()
        death_embed = discord.Embed(description=death)
        await message.channel.send(embed=death_embed)
    elif message.content.startswith("!buffer"):
        args = message.content.split()
        response = None
        if len(args) == 1:
            target = gipped_service + "buffer"
            response = requests.get(gipped_service + "buffer")
        else:
            target = ""
            payload = {}
            if args[1] == "resize":
                try:
                    payload = {"size": int(args[2])}
                    target = gipped_service + "buffer"
                except Exception:
                    pass
            elif args[1] == "length":
                try:
                    payload = {"length": int(args[2])}
                    target = gipped_service + "death"
                except Exception:
                    pass
            response = requests.post(target, json=payload)

        resp = response.text
        buffer_embed = discord.Embed(description=resp)
        await message.channel.send(embed=buffer_embed)
    elif message.content.startswith("!help"):
        response = requests.get(gipped_service + "death/" + message.author)
        death = response.json()
        death_embed = discord.Embed(description=death)
        await message.channel.send(embed=death_embed)

client.run(token)