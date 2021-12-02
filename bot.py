import re
import discord
import json
import random
import emoji
from discord.utils import get

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

#reading from json
'''
with open("config.json") as conf:
	configs = json.load(conf)
	TOKEN = configs["bottoken"]
	emotes = configs["reacts"]
'''


TOKEN = 'Nzg4NTU1OTQ1MTc2OTg5NzM2.X9lN8w.2aWpqXg-6pPZiUJOfY3f1R7paKo'

emotes = [785953585594499112,785953620071940137,785953661271801917,785953681383620628,785953711305916497,785953732159864923,785953770474438666,785953808303652875,785953830336200784,785953848996528168,785955049557065738,785955086072938526,785955110949617694,785955128440127528,785955147611111466,785955165190094868,785955194646167612,785955217380081715,785955247960490084,785955268659380285]
otheremotes = [786349991874527242,785965937790681149,896310029911724044, 915390704832884756]
serveremotes = emotes+otheremotes

concernedonlyexceptions = [379145843200229379, 201715919439790080, 328725093071192066, 243744413061218304, 284528757300264961, 705247998439063562, 272274466107686913]

trollmode = False
exceptionmode = False

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_member_join(member):
	#print("got here")
	role = discord.utils.get(member.guild.roles, name="concerned")
	await member.add_roles(role)
	#print("role added")
	await member.edit(nick="concerned")
	#print("Welcomed new member")

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	global exceptionmode
	if "!em" in message.content and message.author.id in concernedonlyexceptions:
		exceptionmode = not exceptionmode
		print("Exception Mode: ", exceptionmode)

	if message.author.id not in concernedonlyexceptions or not exceptionmode:
		if emoji.emoji_count(message.content) > 0:
			await message.delete()
			return
		msgemotes = re.findall(r'<a?:?\w*:\d*>', message.content)
		msgemotes = [int(e.split(':')[-1].replace('>', '')) for e in msgemotes]
		for x in msgemotes:
			if x not in serveremotes:
				await message.delete()
				return

	global trollmode

	if "!tm" in message.content and message.author.id in concernedonlyexceptions:
		trollmode = not trollmode
		print("Troll Mode: ", trollmode)

	if trollmode and message.author.id == 278396296430092289:
		if random.randint(0,10) < 6:
			await message.delete()

	if "mustard is great" in message.content and message.author.id != 278396296430092289:
		await message.delete()
		role = discord.utils.get(message.guild.roles, name="fake admin role don't give this to anyone")
		await message.author.add_roles(role)


	try:
		for emotename in emotes:
			#emote = get(message.guild.emojis, name=emotename)
			emote = client.get_emoji(emotename)
			if (emote != None):
				await message.add_reaction(emote)
	except:
		pass
	


client.run(TOKEN)
