import discord
from discord.utils import get

client = discord.Client()
TOKEN = 'Nzg4NTU1OTQ1MTc2OTg5NzM2.X9lN8w.2aWpqXg-6pPZiUJOfY3f1R7paKo'

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	emotes = []
	for i in range(1,22):
		if i == 18:
			continue
		s = "concerned" + str(i)
		emotes.append(s)
	for emotename in emotes:
		emote = get(message.guild.emojis, name=emotename)
		await message.add_reaction(emote)

async def get_emoji(guild: discord.Guild, arg):
	 return get(ctx.guild.emojis, name=arg)

client.run(TOKEN)