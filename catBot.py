import discord, os, sys
import os
from discord.ext import commands
import youtube_dl

import time
import random
from datetime import datetime
import os
import asyncio



TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
bot = commands.Bot(command_prefix = "!")






if __name__ == "__main__":
    #dictionary of key words, has some default phrases, and more can be added with !train
    key_words = {"hello": "meeeellow",
                 "ang": "Angelica is my owner i must obey her",
                 "night": "meow sweet dreams",
                 "morning": "meowwwringing",
                 "ring ring": "meow? hello??",
                 "birth": "meow meow meow meow to u!",
                 "meow": "meow"
                 }
    #open existing or make new text file to store key words
    with open('keyWords.txt', "r") as keyWords_file:
        for line in keyWords_file:
            word = line.split("=")
            key = word[0]
            val = word[1]
            key_words[key] = val


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
        duration = time.time() - bot.time
        print(duration)
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

        # stays in bounds
        bot.eat = max(0, bot.eat)
        bot.groom = max(0, bot.groom)
        bot.sleep = max(0, bot.sleep)
        totalEnergy = bot.eat + bot.groom + bot.sleep
        print("totalEnergy: ", totalEnergy)
        print("eat:", bot.eat)
        print("groom:", bot.groom)
        print("sleep:", bot.sleep)


        bot.energy = "DR.  CAT\t\t\t\t\t\t\t\t/ᐠ ̥  ̮  ̥ ᐟ\ ฅ \n\n"
        bot.energy += "feeling:         "
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
        embedVar = discord.Embed(title= bot.energy, color = color_code)
        await ctx.send(embed=embedVar)


    @bot.command(name='feed', help=':: you must feed the cat')
    async def feed(ctx):
        if bot.eat == 9:
            await ctx.send("not hungry :p")
        else:
            bot.eat += 1
            bot.eat = max(0, bot.eat)
            print("eat:", bot.eat)
            await ctx.send("nom nom")

    @bot.command(name='groom', help=':: you must groom the cat')
    async def groom(ctx):
        if bot.groom == 9:
            await ctx.send("no! stop :p")
        else:
            bot.groom += 1
            bot.eat = max(0, bot.groom)
            print("groom:", bot.groom)
            await ctx.send("purr")

    @bot.command(name='sleep', help=':: you must sleep the cat')
    async def sleep(ctx):
        if bot.sleep == 9:
            await ctx.send("not gonna sleep :p")
        else:
            bot.sleep += 1
            bot.eat = max(0, bot.sleep)
            print("sleep:", bot.sleep)
            await ctx.send("Zzz")


    @bot.command(name='train', help=':: train cat new phrases, ex: !train good bye = meow, see ya! :)')
    async def train(ctx, *args):
        if len(args) == 0:
            await ctx.send("meow?")
        else:
            command = " ".join(args)
            i = command.index("=")
            new_key = command[:i]
            new_key = new_key.strip()
            new_val = command[i + 1:]
            new_val = new_val.strip()
            try:
                key_words[new_key] = new_val
            except:  # catch *all* exceptions
                return
            # add key word to a text file to save trained phrases even after bot stops running
            keyWords_file = open('keyWords.txt', "a")
            keyWords_file.write("\n")
            keyWords_file.write(new_key + "=" + new_val)
            keyWords_file.close()




    #for playing audio from youtube
    youtube_dl.utils.bug_reports_message = lambda: ''

    ytdl_format_options = {
        'format': 'bestaudio/best',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
    }

    ffmpeg_options = {
        'options': '-vn'
    }

    ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


    class YTDLSource(discord.PCMVolumeTransformer):
        def __init__(self, source, *, data, volume=0.5):
            super().__init__(source, volume)
            self.data = data
            self.title = data.get('title')
            self.url = ""

        @classmethod
        async def from_url(cls, url, *, loop=None, stream=False):
            loop = loop or asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
            if 'entries' in data:
                # take first item from a playlist
                data = data['entries'][0]
            filename = data['title'] if stream else ytdl.prepare_filename(data)
            return filename



    # joins cat to voice
    @bot.command(name="join", help=":: call cat to join voice")
    async def join(ctx):
        channel = ctx.author.voice.channel
        await channel.connect()


    @bot.command(name="leave", help=":: force cat out of voice")
    async def leave(ctx):
        await ctx.voice_client.disconnect()


    queueList = []
    @bot.command(name='play', help=':: play song')
    async def play(ctx, url="https://www.youtube.com/watch?v=P9AY5rc5M28"):
        voice_client = ctx.message.guild.voice_client
        #add song to queue
        queueList.append(url)
        #if something is playing, tell them their place in queue
        print("is playing: ", voice_client.is_playing())
        if voice_client.is_playing():
            songstext = "song "
            songstext += str(len(queueList))
            songstext += " in queue"
            await ctx.channel.send(songstext)
        # if nothing is playing, then play first song in queue
        if not voice_client.is_playing():
            #get first song and remove it from list
            url = queueList[0]
            queueList.pop(0)
            songstext = "num songs in queue: "
            songstext += str(len(queueList))
            await ctx.channel.send(songstext)
            server = ctx.message.guild
            voice_channel = server.voice_client
            async with ctx.typing():
                filename = await YTDLSource.from_url(url, loop=bot.loop)
                voice_channel.play(discord.FFmpegPCMAudio(executable="C:/Program Files/FFmpeg/bin/ffmpeg.exe", source=filename))




    @bot.command(name='clear', help=':: clears queue')
    async def clear(ctx):
        queueList.clear()
        songstext = "queue is empty"
        await ctx.channel.send(songstext)



    @bot.command(name='stop', help=':: stops the song')
    async def stop(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()



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
        if message.content.startswith("im") or message.content.startswith("Im") or message.content.startswith("I'm"):
            msg = "hi,"
            if message.content.startswith("I'm"):
                msg += message.content[3:]
            else:
                msg += message.content[2:]
            msg += ", im dad"
            await message.channel.send(msg)



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

    # close text file
    keyWords_file.close()
