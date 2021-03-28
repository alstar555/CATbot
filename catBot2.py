import discord, asyncio, os, platform, sys
from discord.ext.commands import Bot
from discord.ext import commands
import random
from datetime import datetime
from discord import Intents
intents = Intents.all()
import time


if not os.path.isfile("config.py"):
	sys.exit("'config.py' not fvirtualenv venvound! Please add it and try again.")
else:
	import config

TOKEN = config.TOKEN
GUILD = config.GUILD
bot = commands.Bot(command_prefix = "!")





if __name__ == "__main__":
    #dictionary of key words, has some default phrases, and more can be added with !train
    key_words = {"hello": "meeeellow",
                 "ang": "Angelica is my owner i must obey her",
                 "night": "meow sweet dreams",
                 "morning": "meowwwringing",
                 "ring ring": "meow? hello??",
                 "birth": "meow meow meow meow to u!",
                 "cat": "that's me!",
                 "meow": "meow"
                 }

    bot.time = time.time()
    bot.count = 0
    bot.feeling = ":)"
    bot.eat = 9
    bot.groom = 9
    bot.sleep = 9
    bot.representation = " ♡ "

    @bot.event
    async def on_ready():
        print(f'{bot.user.name} has connected to Discord!')

    @bot.event
    async def on_message(message):
        #don't reply to bots
        if message.author == bot.user or message.author.bot:
            return
        await bot.process_commands(message)

    #commands
    @bot.command(name='energy', help=":: displays cat's energy levels")
    async def energy(ctx):
        # stays in bounds
        bot.eat = max(0, bot.eat)
        bot.groom = max(0, bot.groom)
        bot.sleep = max(0, bot.sleep)
        print("eat2:", bot.eat)
        totalEnergy = bot.eat + bot.groom + bot.sleep
        duration = time.time() - bot.time
        print(duration)
        if totalEnergy > 0:
            #feed every 30 min
            if bot.eat > 0:
                bot.eat -= int(duration // 10)
                #bot.eat -= duration//1800
            #groom every hour
            if bot.groom > 0:
                bot.groom -= int(duration//15)
            #sleep every 5 hours
            if bot.sleep > 0:
                bot.sleep -= int(duration//25)
            bot.time = time.time()

        bot.energy = "feeling:         "
        print("totalEnergy: ", totalEnergy)
        if totalEnergy <= 0:
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


        #colors gradually change based on lives
        color_code = 0xA6E516
        for x in range(27-totalEnergy):
            color_code -= 1000
        embedVar = discord.Embed(title=bot.energy, color = color_code)
        await ctx.send(embed=embedVar)


    @bot.command(name='feed', help=':: you must feed the cat')
    async def feed(ctx):
        if bot.eat == 9:
            await ctx.send("not hungry :p")
        else:
            bot.eat += 1
            print("eat:", bot.eat)
            await ctx.send("nom nom")

    @bot.command(name='groom', help=':: you must groom the cat')
    async def groom(ctx):
        if bot.groom == 9:
            await ctx.send("no! stop :p")
        else:
            bot.groom += 1
            print("groom:", bot.groom)
            await ctx.send("purr")

    @bot.command(name='sleep', help=':: you must sleep the cat')
    async def sleep(ctx):
        if bot.sleep == 9:
            await ctx.send("not gonna sleep :p")
        else:
            bot.sleep += 1
            print("sleep:", bot.sleep)
            await ctx.send("Zzz")


    @bot.command(name='train', help=':: train cat new phrases, ex: !train good_bye = meow,_see_ya')
    async def train(ctx, command="none"):
        if command == "none":
            await ctx.send("meow?")
        else:
            i = command.index("=")
            new_key = command[:i]
            new_key = new_key.replace("_", " ")
            new_val = command[i+1:]
            new_val = new_val.replace("_", " ")
            key_words[new_key] = new_val

    #joins cat to voice
    @bot.command(name = "join")
    async def join(ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

    @bot.command(name="leave")
    async def leave(ctx):
        await ctx.voice_client.disconnect()


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
        for key in key_words:
            if key in message.content:
                await message.channel.send(key_words[key])
        if "copy" in message.content:
            await message.channel.send(message.content)


        #randomly chimes into convo
        elif bot.count % 60 == 0:
            await message.channel.send("meow pay attention to me")
        elif bot.count % 100 == 0:
            await message.channel.send("meow feed me!")
        elif bot.count % 20 == 0:
            await message.channel.send("meow")
        await bot.process_commands(message)



    #run bot
    bot.run(TOKEN)
