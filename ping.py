import asyncio
import datetime
import json
from leaderboard import Leaderboard

#TODO: Use something other than asyncio.sleep() cus that goes out of sync pretty quickly
class Ping():
	def __init__(self, msg_obj, user_message, mentions, interval, client):
		self.msg_obj = msg_obj
		self.user_message = user_message
		self.mentions = mentions
		self.interval = interval
		self.client = client
		self.send_msg = None
		self.is_stopped = False 
		self.ping_count = 0

	async def construct_message(self):
		mention_str = ''
		if self.is_multi_ping():
			for mention in range(0, len(self.mentions) - 1):
				mention_str += self.mentions[mention] + ', '
			mention_str += self.mentions[len(self.mentions) - 1]
		else:
			mention_str = self.mentions[0]

		author_name = self.msg_obj.author.display_name
		return mention_str + ': {0} says {1}'.format(author_name, self.user_message)

	def get_author(self):
		return self.msg_obj.author

	def is_multi_ping(self):
		return len(self.mentions) > 1

	def get_server(self):
		return self.msg_obj.server

	async def start(self):
		if self.send_msg == None:
			print("Constructing message")
			self.send_msg = await self.construct_message()		

		await asyncio.sleep(self.interval) #initial sleep

		while not self.is_stopped:
			await self.client.send_message(self.msg_obj.channel, self.send_msg)
			print("Ping sent at {0}".format(datetime.datetime.now()))
			self.ping_count += 1
			await asyncio.sleep(self.interval)	

	async def stop(self):
		channel = self.msg_obj.channel
		message = "Pinged {0} times. :)".format(self.ping_count)
		self.is_stopped = True
		Leaderboard.try_add_to_leaderboard(self.get_server().id, self)	
		await self.client.send_message(channel, message) 

	def asJSON(self):
		return {"author" : self.get_author().display_name, "avatar" : self.get_author().avatar_url, "user_message" : self.user_message, "interval" : self.interval, "mentions" : self.mentions, "ping_count" : self.ping_count}
