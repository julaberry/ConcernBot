import re
import discord
from dotenv import load_dotenv
import os
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

load_dotenv("config.env")
TOKEN = os.getenv("TOKEN")
REACTS = os.getenv("REACTS")
EMOTES = os.getenv("EMOTES")
SUPERS = os.getenv("SUPERS")
TROLLS = os.getenv("TROLLS")


emotes = []
otheremotes = []
serveremotes = []
concernedonlyexceptions =[]
trolledusers = []


def refresh():
	global emotes
	global otheremotes
	global serveremotes
	global concernedonlyexceptions
	global trolledusers
	with open(REACTS) as f:
		emotes = [int(line.rstrip()) for line in f]
	with open(EMOTES) as f:
		otheremotes = [int(line.rstrip()) for line in f]
	serveremotes = emotes + otheremotes
	with open(SUPERS) as f:
		concernedonlyexceptions = [int(line.rstrip()) for line in f]
	with open(TROLLS) as f:
		trolledusers = [int(line.rstrip()) for line in f]

refresh()

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

	if "!refresh" in message.content and message.author.id in concernedonlyexceptions:
		refresh()
		print("Refreshed emotes and exceptions.")
		await message.delete()
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

	if trollmode and message.author.id in trolledusers:
		if random.randint(0,10) < 6:
			await message.delete()

	if "mustard is great" in message.content and message.author.id not in trolledusers:
		await message.delete()
		role = discord.utils.get(message.guild.roles, name="fake admin role don't give this to anyone")
		await message.author.add_roles(role)


	try:
		for emotename in emotes:
			#emote = get(message.guild.emojis, name=emotename)
			emote = client.get_emoji(emotename)
			if (emote != None):
				await message.add_reaction(emote)
	except Exception as e:
		print(e)
	


client.run(TOKEN)
