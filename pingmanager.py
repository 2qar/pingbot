import asyncio

async def stop_pinging_if_victim_or_author(message, pings):
	for ping in range(0, len(pings)):
		print("ping ", ping)
		if message.server == pings[ping].get_server():
			should_remove = False
			author = message.author
			current_ping = pings[ping]
	
			if author.mention in current_ping.mentions:
				should_remove = True	
				print("Victim {0} sent message, cancelling ping.".format(author.mention))
			elif author.display_name == current_ping.get_author().display_name and message.content == "stop":
				should_remove = True	
				print("Author {0} cancelled ping.".format(author.display_name))
			
			if should_remove:
				await current_ping.stop()
				del pings[ping]
				ping -= 1
