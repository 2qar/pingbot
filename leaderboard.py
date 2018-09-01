from config import error
from discord import Embed
from discord import Colour
import pingutils
import json
class Leaderboard:
	colors = [Colour.gold(), Colour.light_grey(), Colour.dark_orange()]
	async def check_server_leaderboard(msg_obj, client):
		try:
			data = None
			with open("leaderboards/" + msg_obj.server.id + ".json") as file:
				data = json.load(file)
			for ping in range(len(data)):
				await client.send_message(msg_obj.channel, embed=Leaderboard.embed_constructor(data[ping], msg_obj.server, ping + 1, Leaderboard.colors[ping]))	
		except Exception as e: 
			print(e)
			await client.send_message(msg_obj.channel, error + "No leaderboard for this server!")

	#TODO: Maybe divide interval by ping_count to determine a ping's "value" and compare values for leaderboard spots
		# maybe only use the worth as a modifier to multiply ping_count by for a "value"
	def try_add_to_leaderboard(server_id, ping):
		# try to open an existing leaderboard and if possible add this ping
		try:
			leaderboard_path = "leaderboards/" + server_id + ".json"
			print("checking if ping should be added")
			data = None
			insert_index = -1
			ping_json = ping.asJSON()

			with open(leaderboard_path) as file:
				data = json.load(file)
				ping_count = ping_json['ping_count']
				for i in range(0, len(data)):
					if data[i]['ping_count'] < ping_count:
						insert_index = i
						print("ping marked for insertion")
						break
				if insert_index == -1 and len(data) < 3:
					insert_index = -2

			# add the ping if insert_index was actually changed
			if insert_index > -1:
				with open(leaderboard_path, "w") as outfile:
					data.insert(insert_index, ping_json)
					if len(data) == 4:
						del data[3]
					json.dump(data, outfile)
					print("ping inserted")
			# if there's room for the ping, just add it 
			elif insert_index == -2:
				with open(leaderboard_path, "w") as outfile:
					data.append(ping_json)
					print("ping appended")
					json.dump(data, outfile)

		# if there's no existing leaderboard for this server, make one and add this ping
		except Exception as e:
			print("error ", e)
			print("making leaderboard")
			with open("leaderboards/" + server_id + ".json", "w") as outfile:
				data = []
				data.append(ping.asJSON())
				json.dump(data, outfile)	

	#TODO: Add discriminator to the JSON
	def embed_constructor(ping_json, server, num, color):
		embed = Embed()
		author = ping_json["author"]
		author_icon = ping_json["avatar"]

		embed.colour = color
		embed.set_author(name="#{0}".format(num))
		embed.set_thumbnail(url=author_icon)
		embed.add_field(name="Author", value = author)
		embed.add_field(name="Message", value=ping_json["user_message"])
		mentions = ping_json["mentions"]
		embed.add_field(name="Mentions", value=pingutils.get_formatted_name_list(server, mentions))
		embed.add_field(name="Ping Count", value=ping_json["ping_count"])
		interval = ping_json["interval"]
		embed.add_field(name="Interval", value="{0} seconds".format(interval))
		return embed	
