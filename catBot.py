import discord
from discord.ext import commands

"""declaring variables"""
client = discord.Client()
#TOKEN = "add discord token key here"
TOKEN = "add token"
print('lets go')
client.count = 0


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    client.count += 1
    if message.author == client.user:
        return
    """respond to key words"""
    if "hello" in message.content:
        await message.channel.send("meow world i am CAT")
    elif "night" in message.content:
        await message.channel.send("meow sweet dreams")
    elif "meow" in message.content:
        await message.channel.send("meow meow")
    elif client.count % 20 == 0:
        await message.channel.send("meow pay attention to me")
    elif client.count % 35 == 0:
        await message.channel.send("meow feed me!")
    elif client.count % 5 == 0:
        await message.channel.send("meow")

client.run(TOKEN)
