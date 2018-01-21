import discord
import random
from discord.ext import commands
from apiclient.discovery import build
import asyncio
import http.client
from Util.FilePrinter import *
from Util.PokemonJson import getGif

class FlavorTexts:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(hidden = True)
	async def Runs(self):
	    await self.bot.say("a list of completed DarkSouls3 Challenge runs Check them out Here! https://plus.google.com/u/0/+ChrisVengeance")

	@commands.command(hidden = True)
	async def Vgs(self):
	    await self.bot.say("Here's a Link to Light's personal Videogame Sountrack playlist! https://www.youtube.com/playlist?list=PLL46KqJ0EiNe1F3pN4HfQTKcDjy5sy0vh")

	@commands.command()
	async def fml(self):
		'Returns a Random Post from fmylife.com'
		await self.bot.say("*{}*".format(fmlText()))

	@commands.command()
	async def conch(self, question : str):
	    'Ask the Magic Conch a Question'
	    conn = http.client.HTTPSConnection("8ball.delegator.com")
	    question = urllib.parse.quote(question)
	    conn.request('GET', '/magic/JSON/' + question)
	    response = conn.getresponse()
	     
	    if response.status == http.client.OK:
	        lines = response.read().decode(encoding='UTF-8').split('\n')
	        await self.bot.say("*" + lines[3][15:-2] + "*")
	        await self.bot.say("The Conch has Spoken!")
	     
	    conn.close()

	@commands.command()
	async def wyr(self):
		result = wouldYouRather()
		while(str(result[0][0]) == "" or str(result[1][0]) == ""):
			result = wouldYouRather()
		await self.bot.say("Would you Rather...\n*" + result[0][1] + "* or *" + result[1][1] + "*")
		await asyncio.sleep(5)
		await self.bot.say("People say...\n*" + str(result[0][0]) + "* and *" + str(result[1][0]) + "*")

	@commands.command()
	async def rps(self, player_input = None):
		"Allows the player to play Rock, Paper, Scissors with the Bot. Simply enter, R, P or S to play!"
		if player_input == None or player_input not in ['R', 'P', 'S']:
			await self.bot.say("You need to put in either (R)ock, (P)aper, or (S)cissors")
			return
		Values = {"R":":right_facing_fist:", "P":":raised_back_of_hand:", "S":":v:"}
		bot_choice = random.choice(["R", "P", "S"])
		await self.bot.say("You throw {}\nI throw {}".format(Values[player_input], Values[bot_choice]))
		if(bot_choice == player_input):
			await self.bot.say("Its a Tie, we both put {}".format(Values[player_input]))
		if bot_choice == "R":
			if player_input == "P":
				await self.bot.say("**You Win!**")
			if player_input == "S":
				await self.bot.say("I Win! :stuck_out_tongue:")
		if bot_choice == "P":
			if player_input == "S":
				await self.bot.say("**You Win!**")
			if player_input == "R":
				await self.bot.say("I Win! :stuck_out_tongue:")
		if bot_choice == "S":
			if player_input == "R":
				await self.bot.say("**You Win!**")	
			if player_input == "P":
				await self.bot.say("I Win! :stuck_out_tongue:")

	@commands.command(pass_context = True)
	async def rate(self, ctx):
	    "Rates the Player"
	    if ctx.message.author.id == '226028320104382464':
	    	await self.bot.say("{} is actually god".format(ctx.message.author.name))
	    	return
	    await self.bot.say("{} is kinda cool".format(ctx.message.author.name))

	@commands.command(Hidden = True)
	async def kys(self):
	    await self.bot.say(random.choice([
	    	"Hey Mean!",
	    	"How about... no",
	    	"Sure, i heard cyanide works wonders",
	    	"Im Sorry, That goes against my programming"]))

	@commands.command(hidden = True)
	async def kms(self):
	    await self.bot.say(random.choice([
	    	"More souls for me then (:",
	    	"Don't Die",
	    	"Bet",
	    	"Here's a noose then",
	    	"Good :)"]))

	@commands.command(pass_context = True)
	async def image(self, ctx, *toGoogle : str):
		"Returns the First Found Image on Google Images for this Input"
		service = build("customsearch", "v1", developerKey="AIzaSyB-ILulo61cnlt68SUP6giJwmyI3S6JgbQ")

		googleSearch = " ".join(toGoogle)
		res = service.cse().list(
		    q=googleSearch,
		    cx='001619551424816794764:dqn9nzjp57a',
		    searchType='image',
		    num=1,
		    fileType='jpg',
		    safe= 'high'
		).execute()

		if not 'items' in res:
		    await self.bot.say('ERROR')
		else:
		    for item in res['items']:
		        await self.bot.say(item['link'])

	@commands.command(pass_context = True)
	async def gif(self, ctx, *toGoogle : str):
		"Returns the First Found Image on Google Images for this Input"
		await self.bot.say(getGif("%20".join(toGoogle)))

	@commands.command(pass_context = True)
	async def punch(self,ctx, member : str):
	    'Adds Emotion'
	    await self.bot.say(":punch: *{} punched {}* :punch:".format(ctx.message.author.name, member))

	@commands.command(pass_context = True)
	async def kiss(self,ctx, member : str):
	    'Adds Emotion'
	    await self.bot.say(":heart: *{} Kissed {}* :heart:".format(ctx.message.author.name, member))

	@commands.command()
	async def lmgtfy(self, * toGoogle : str):
		'Returns a Link to a "Let me Google That For You" Page'
		await self.bot.say("http://lmgtfy.com/?q={}".format("+".join(toGoogle)))

	@commands.command()
	async def funify(self, * text : str):
		'Funifies a given text input'
		finalOutput = ""
		for x in text:
			for character in x:
				for i in range(0,int(random.random() * 2 + 1),1):
					finalOutput += random.choice([character.lower()] * 10 + [character.upper()] * 10 + [character.lower() + random.choice("1234567890-=[];',./!@#$%^&(_+{}: ")] + [character.upper() + random.choice("1234567890-=[];',./!@#$%^&(_+{}: ")])
			finalOutput += " "
		await self.bot.say(finalOutput)

	@commands.command()
	async def choose(self, * options : str):
		'Chooses from a set of things'
		await self.bot.say(random.choice(["Hmm, tough choice", "Oh, Thats easy", "Alright, picked one"]))
		await self.bot.say("Chosen Option: " + random.choice(options))

	@commands.command(pass_context = True)
	async def luck(self,ctx):
		'Returns the Player\'s Luck'
		luck = round(random.random() * 100,2)
		if 0 <= luck <= 20:
			text = "Completly Horrible"
		elif 20 <= luck <= 40:
			text = "Pretty Bad"
		elif 40 <= luck <= 60:
			text = "Not Bad"
		elif 60 <= luck <= 80:
			text = "Pretty Good"
		elif 80 <= luck <= 100:
			text = "HAX"
		else:
			text = "Literally Impossible"

		await self.bot.say("{0.message.author.name}'s luck is {1} out of 100, which is **{2}**".format(ctx,luck,text))

	@commands.command(pass_context = True)
	async def Marry(self,ctx, member : str):
		'Adds Emotion'
		await self.bot.say(":ring: *{} Married {}* :ring:".format(ctx.message.author.name, member))
		await self.bot.say("You may now kiss the bride!")
	
	@commands.command(pass_context = True)
	async def hug(self,ctx, member : str):
		'Adds Emotion'
		await self.bot.say(":hugging: *{} Hugged {}* :hugging:".format(ctx.message.author.name, member))

	# @commands.command(hidden = True)
	# async def boss(self, old, correct):
	# 	new = []
	# 	cur = 0
	# 	for c in old:
	# 		if correct[cur] == '0':
	# 			new.append(self.inc(c))
	# 		else:
	# 			new.append(c)
	# 		cur += 1
	# 	await self.bot.say("".join(new))

	# def inc(self, c):
	# 	values = {"A":"D", "D":"S", "S":"B", "B":"E", "E":"F", "F":"A"}
	# 	return values[c]

def setup(bot):
	bot.add_cog(FlavorTexts(bot))