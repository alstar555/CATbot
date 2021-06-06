# CatBot 

CAT is a customizable bot for the discord platform. 
When added to a server, CAT will meow every x amount of messages. He will also chime into the conversation when triggered by certain key words.
It also has extra features such as lives, feeding, grooming, and sleeping. He can be trained to relpy to custom phrases with the !train command.
Can also act as music bot.

A demo of CAT can be seen by joining this discord server: 
https://discord.gg/fmUTnXYF

note that CAT does not run 24/7

Add Cat bot to your own discord server with this link:
https://discord.com/api/oauth2/authorize?client_id=824824038228099103&permissions=1513483888&scope=bot 




# Features

* meows

* replies to keywords

* keywords can be customized with !train command

* responds to commands

* plays music and meow in voice channel


cat must be taken care of in order for him not to loose his 9 lives
| Command | Description |
| ------------- | ----- |
|  !train       | train cat new phrases, ex: !train good_bye = meow,_see_ya  |
|  !feed |  cat must be fed every 30 min  |
|  !groom |  cat must be groomed every hour  |
|  !sleep | cat must sleep every 5 hours  |
| !play   | plays song from youtube url
|  !help | help command to see description of all commands  |


# Requirements 
* Python 
* Discord.py library
* PyNaCl library

# Set Up
If you want to clone this repo and host the bot yourself:

You need to create a discord account to run this bot and create a discord server to place the bot in.

In the discord developer portal, create a new application and add the bot to your server

Run this python code in a ide such as pycharm.

In the config.py section, add your bot's token code, your server's guild code, and the prefix to command the bot.

For example:

TOKEN = "XXXXXXX1234"

GUILD = "12345678"

prefix = "!"

Run the program and the bot should appear in your server!


# ToDO

updates/ideas in development:
 
* music cat bot is in development/ still glitchy
* roles
* name cat

