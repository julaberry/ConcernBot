import discord
import json
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
	'''
	emotes = []
	for i in range(1,22):
		if i == 18:
			continue
		s = "concerned" + str(i)
		emotes.append(s)
	'''
	try:
		for emotename in emotes:
			#emote = get(message.guild.emojis, name=emotename)
			emote = client.get_emoji(emotename)
			if (emote != None):
				await message.add_reaction(emote)
	except:
		pass
	


client.run(TOKEN)
