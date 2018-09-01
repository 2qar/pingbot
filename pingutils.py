def get_name_from_mention(server, mention):
	trimmed_id = mention[2:len(mention) - 2]
	if "!" in trimmed_id:
		return server.get_member(trimmed_id[1:len(trimmed_id) - 1])	
	else:
		return trimmed_id

def get_formatted_name_list(server, mentions):
	mention_str = ""
	for mention in range(0, len(mentions) - 1):
		mention_str += mentions[mention] + ", "	
	mention_str += mentions[len(mentions) - 1]
	return mention_str
