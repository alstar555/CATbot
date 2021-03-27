import discord, asyncio, os, platform, sys
from discord.ext.commands import Bot
from discord.ext import commands
import random
from datetime import datetime
import time


if not os.path.isfile("config.py"):
	sys.exit("'config.py' not found! Please add it and try again.")
else:
	import config

TOKEN = config.TOKEN
GUILD = config.GUILD
bot = commands.Bot(command_prefix = "!")





if __name__ == "__main__":

    bot.time = time.time()
    bot.count = 0

    @bot.event
    async def on_ready():
        print(f'{bot.user.name} has connected to Discord!')

    @bot.event
    async def on_message(message):
        #don't reply to bots
        if message.author == bot.user or message.author.bot:
            return
        await bot.process_commands(message)

    bot.feeling = ":)"
    bot.eat = 9
    bot.groom = 9
    bot.sleep = 9
    bot.representation = " ♡ "


    #commands
    @bot.command(name='energy', help=":: displays cat's energy levels")
    async def energy(ctx):
        duration = time.time() - bot.time
        print(duration)
        #feed every 30 min
        bot.eat -= int(duration // 60)
        #bot.eat -= duration//1800
        bot.time = time.time()
        #groom every hour
        bot.groom -= int(duration//36000)
        #sleep every 5 hours
        bot.sleep -=  int(duration//180000)
        if duration > 180000:
            bot.time = time.time()

        bot.energy = "feeling:         "
        totalEnergy = bot.eat+ bot.groom + bot.sleep
        if totalEnergy == 0:
            bot.energy += "dead"
        elif totalEnergy > 24:
            bot.energy += ":)"
        elif totalEnergy < 9:
            bot.energy += ":("
        else:
            bot.energy += ":|"
        bot.energy += "\neat:       "
        bot.energy += bot.eat * bot.representation
        bot.energy += "\ngroom: "
        bot.energy += bot.groom * bot.representation
        bot.energy += "\nsleep:   "
        bot.energy += bot.sleep * bot.representation

        await ctx.send(bot.energy)

    @bot.command(name='feed', help=':: you must feed the cat')
    async def feed(ctx):
        if bot.eat == 10:
            await ctx.send("not hungry :p")
        else:
            bot.eat += 1
            await ctx.send("nom nom")

    @bot.command(name='groom', help=':: you must groom the cat')
    async def groom(ctx):
        if bot.groom == 10:
            await ctx.send("no! stop :p")
        else:
            bot.groom += 1
            await ctx.send("purr")

    @bot.command(name='sleep', help=':: you must sleep the cat')
    async def sleep(ctx):
        if bot.sleep == 10:
            await ctx.send("not gonna sleep :p")
        else:
            bot.sleep += 1
            await ctx.send("Zzz")




    #events
    @bot.event
    async def on_message(message):
        #protect from messaging himself
        if message.author == bot.user or message.author.bot:
            return

        random.seed(datetime.now())
        randomNum = random.randrange(1, 10)

        if bot.count >= 100:
            bot.count = 0
        else:
            bot.count += 1

        # respond to keywords
        if "ang" in message.content:
            await message.channel.send("angelica is my owner i obey her")
        elif "copy" in message.content:
            await message.channel.send(message.content)
        elif "night" in message.content:
            await message.channel.send("meow sweet dreams")
        elif "birthday" in message.content:
            await message.channel.send("meow meow meow meow to u!")
        elif "meow" in message.content:
            meows = randomNum * "meow "
            await message.channel.send(meows)
        elif "cat" in message.content:
            await message.channel.send("that's me!")
        elif bot.count % 60 == 0:
            await message.channel.send("meow pay attention to me")
        elif bot.count % 100 == 0:
            await message.channel.send("meow feed me!")
        elif bot.count % 20 == 0:
            await message.channel.send("meow")
        await bot.process_commands(message)



    #run bot
    bot.run(TOKEN)
