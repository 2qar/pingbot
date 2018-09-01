from config import *
import discord
import asyncio
import logging

#TODO: Combine these two into one pingmanager file if nothing gets added to them later
import pingbuilder
import pingmanager
import leaderboard

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

pings = []

@client.event
async def on_ready():
	print("Ready! :)")

@client.event
async def on_message(message):
	if not message.author.bot and len(pings) > 0:
		await pingmanager.stop_pinging_if_victim_or_author(message, pings)	
	if message.content.startswith('tell'):
		await pingbuilder.create_ping(message, client, pings)	
	elif message.content.startswith("leaderboard"):
		await leaderboard.Leaderboard.check_server_leaderboard(message, client)

client.run(token)
