import random
import asyncio
import aiohttp
import json
import datetime
import youtube_dl
import discord
from discord.ext import commands
from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = ("?", "!")
TOKEN = "NDYyMzEzNjI5MDU3MDI0MDIw.DhkzNQ.5A2-0P99iQjOTnFHEfheVnKyjwY"  # Get at discordapp.com/developers/applications/me

client = Bot(command_prefix=BOT_PREFIX)

players = {}

@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    print("Logged in as " + client.user.name)

@client.command()
async def square(number):
    squared_value = int(number) * int(number)
    await client.say(str(number) + " squared is " + str(squared_value))

@client.command()
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])

@client.command()
async def fetchmesomebovril():
    await client.say("A cup of bovril, sir")

@client.command()
async def nuke17032002():
    while True:
        await client.say("NUKE")
        await asyncio.sleep(0.02)

@client.command()
async def election():
    months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    now = datetime.datetime.now()
    numbdays = months[now.month - 1] - now.day + 1
    msg = 'There are ' + str(numbdays) + ' days until the next election'
    await client.say(msg)

@client.command(pass_context=True)
async def join(ctx):
    author = ctx.message.author
    voice_channel = author.voice_channel
    vc = await client.join_voice_channel(voice_channel)

@client.command(pass_context = True)
async def leave(ctx):
    for x in client.voice_clients:
        if(x.server == ctx.message.server):
            return await x.disconnect()

@client.command(pass_context = True)
async def play(ctx, url):
    for x in client.voice_clients:
        if(x.server == ctx.message.server):
            player = await x.create_ytdl_player(url)
            player.start()

'''
@client.command(pass_context = True)
async def reset(ctx):
    for x in client.voice_clients:
        if(x.server == ctx.message.server):
            return await x.disconnect()
    await asyncio.sleep(2)
    author = ctx.message.author
    voice_channel = author.voice_channel
    vc = await client.join_voice_channel(voice_channel)
'''

'''
@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voicechannel
    await client.join_voice_channel(channel)

@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

@client.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()
'''

@client.event
async def on_message(message):
    now = datetime.datetime.now()
    if message.author == client.user:
        return
    if message.content.startswith('!leader') and now.day == 3:
        msg = '{0.author.mention}'.format(message)
        await client.send_message(client.get_channel("368857820139094019"), msg)
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
        await client.process_commands(message)
    await client.process_commands(message)

async def list_servers():
    await client.wait_until_ready()
    months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        now = datetime.datetime.now()
        if now.day == months[now.month - 1] - 6:
            await client.send_message(client.get_channel('368857820139094019'), 'There will be an election in 1 week')
        if now.day == months[now.month - 1] - 2:
            await client.send_message(client.get_channel('368857820139094019'), 'There will be an election in 3 days')
        if now.day == 3:
            await client.send_message(client.get_channel('368857820139094019'), '@everyone It is time for an election')
            await client.send_message(client.get_channel('368857820139094019'), 'React to the candidate you wish to vote for: ')
        await asyncio.sleep(86400)

client.loop.create_task(list_servers())
client.run(TOKEN)
