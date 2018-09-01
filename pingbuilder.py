from myconfig import *
from ping import Ping

async def create_ping(message, client, pings):
	msg_content = message.content
	print("Message \"{0}\" being made into a ping".format(msg_content))
	channel = message.channel

	# don't let an author create multiple pings in one server
	if len(pings) > 0:
		for ping in pings:
			if ping.get_author() == message.author and ping.get_server == message.server:
				msg = 'Hey you, you already have a ping in this server! :angry:'
				await client.send_message(channel, msg)
				return 

	msg = "" 
	msg_start = msg_content.find('"')
	msg_end = msg_content.rfind('"')

	if msg_start != -1 and msg_end != -1:
		msg_start += 1
		msg = msg_content[msg_start:msg_end]
	else:
		return_msg = error + 'No message given / missing a quotation mark!'
		await client.send_message(channel, return_msg)
		return

	mentions = []

	index = 0

	while msg_content.find('<', index, msg_start) != -1:
		mention_start = msg_content.find('<', index)
		mention_end = msg_content.find('>', index) + 1

		mention = msg_content[mention_start:mention_end]
		print(mention)

		if not mention in mentions:
			mentions.append(mention)

		index = mention_end

	if not mentions:
		return_msg = error + 'No users to ping!'
		await client.send_message(channel, return_msg)
		return
	elif client.user.mention in mentions:
		return_msg = error + 'Don\'t ping me :rage:'
		await client.send_message(channel, return_msg)
		return

	interval_start = msg_content.rfind('every', msg_end)
	interval_end = msg_content.rfind('seconds', msg_end)

	if interval_start != -1 and interval_end != -1:
		interval_start += 6
		interval_end -= 1
	else:
		return_msg = error + 'You didn\'t say \"every\" or \"seconds\", silly. ;)'
		await client.send_message(channel, return_msg)
		return 

	interval = int(msg_content[interval_start:interval_end])

	if interval == 1:
		return_msg = 'No 1 second messages allowed. :rage:'
		await channel.send_message(channel, return_msg)
		return	

	pingie = Ping(message, msg, mentions, interval, client) 
	pings.append(pingie)
	await client.send_message(channel, success + 'Gotcha. :)')
	await pingie.start()
