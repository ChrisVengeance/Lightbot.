import discord
from discord.ext import commands
import random
import traceback

from Tournament import *

from Redeem.RedeemUtil import *
from Redeem.ActiveCodes import *
from Redeem.RewardTable import *

class Tournament:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context = True)
	async def data(self, ctx, name = "BLANKNAME"):
	    """Returns Player Data"""
	    if name == "Botfuzzy77":
	        await self.bot.say("I am a Bot")
	        return
	    try:
	        if name == "BLANKNAME":
	            x  = open("./Sync./" + ctx.message.author.name + ".txt",'r')
	            name = x.read()
	            x.close
	        f = open("./OutputFolder./" + name + ".txt",'r')
	        result = f.read()
	        f.close()
	    except Exception:
	        traceback.print_exc()
	        await self.bot.say('Sorry, I couldnt find that Player')
	        return

	    await self.bot.say(result)
	    f.close()

	@commands.command()
	async def ranking(self, To:int = 5, From:int = 1):
	    """Returns the Current Server Rankings"""
	    try:
	        result = ""
	        From = From-1
	        f = open("./OutputFolder./" + "Ranking" + ".txt",'r')
	        while(From > 0):
	            f.readline()
	            From -= 1
	            To -= 1
	        for i in range(From,To):
	            result += f.readline()
	        f.close()
	    except Exception:
	        traceback.print_exc()
	        await self.bot.say("Invalid Input")
	        return
	    try:
	    	await self.bot.say(result)
	    except Exception:
	    	await self.bot.say("Output is Too Long")

	@commands.command()
	async def tournaments(self):
	    '''Returns All tournament info'''
	    f = open("./OutputFolder./" + "Tournaments" + ".txt",'r')
	    result = f.read()
	    f.close()
	    await self.bot.say(result)

	@commands.command(pass_context = True)
	async def sync(self, ctx, IGName : str):
	    '''Syncs you Discord Account with the Given IG Name'''
	    if isSynced(IGName):
	        await self.bot.say("That name has already been Synced")
	        return
	    f = open("./Sync./" + ctx.message.author.name + ".txt",'w')
	    f.write(IGName)
	    f.close()
	    await self.bot.say("Sync Completed")

	@commands.command(pass_context = True)
	async def redeem(self, ctx, Code:int = 0):
		'''Redeems a Given Code for the prize it contains'''
		CollectRDCodes()
		res = isValid(Code)
		ValidRes = ["HALF", "ONE", "TWO", "FIVE", "TEST"]
		if res in ValidRes:
			RTable = RewardTable()
			if res == "TEST":
				prize = RTable.getDrop("ONE")
			else:
				prize = RTable.getDrop(res)
				f = open("Usedcodes.txt", 'a')
				f.write("{}\n".format(Code))
				f.close()
		elif Code == 0:	
			await self.bot.say("You Need to Give an Actualy Code. Ex. '!redeem 75892749275'")
			return
		else:
			await self.bot.say("{} is an {} Code".format(Code,res))
			return

		await self.bot.say("{} won...".format(ctx.message.author.mention))
		if res == "TEST":
			await self.bot.say("*With Testing Code*")
		await self.bot.say(prize)

		if "TEST" not in res:
			f = open("Winners.txt", 'a')
			f.write("{} won\n{}\nwith Code {}\n".format(ctx.message.author, str(prize), Code))
			f.close()

	@commands.command(pass_context = True)
	async def sell(self, ctx, Code:int = 0):
		'Used to Sell a Code instead of Redeeming it'
		if(Code == "soul") or (Code == "Soul"):
			await self.bot.say("Sorry, I dont accept that currency, try downstairs")
			return

		CollectRDCodes()
		res = isValid(Code)

		ValidRes = ["One", "TWO", "FIVE", "TEST"]
		if res in ValidRes:
			RTable = RewardTable()
			if res == "TEST":
				prize = RTable.getDrop("TWO")
			else:
				prize = RTable.getDrop(res)
				f = open("Usedcodes.txt", 'a')
				f.write("{}\n".format(Code))
				f.close()
		elif Code == 0:	
			await self.bot.say("You Need to Give an Actualy Code. Ex. '!redeem 75892749275'")
			return
		else:
			await self.bot.say("{} is an {} Code".format(Code,res))
			return

		await self.bot.say("{} sold {} for...".format(ctx.message.author.mention, prize.Name))
		if res == "TEST":
			await self.bot.say("*With Testing Code*")
		await self.bot.say("${}".format(prize.Value * .75))

		if "TEST" not in res:
			f = open("Winners.txt", 'a')
			f.write("{} cashed in {} with Code {}\n".format(ctx.message.author, ret, Code))
			f.close()

	@commands.command()
	async def prize(self):
		'Returns a Link to where all the Current Prizes can be found'
		await self.bot.say("https://gist.github.com/77Wertfuzzy77/30567d6ea547adce48042b86eec0573d")


def setup(bot):
	bot.add_cog(Tournament(bot))

# /broadcast [&cTournament&f] &aMay Flowers Tournament http://limitlessmc.challonge.com/vm2cjefi
# /bcast [&cTournament&f] &aNoob Tournament This Weekend! http://limitlessmc.challonge.com/k4ssiskw
# /bcast [&cTournament&f] &aLv 100 Tournament This Weekend! http://limitlessmc.challonge.com/4h5lg5li
# /bcast [&cTournament&f] &aLevel 1 Tournament on the 14th! http://limitlessmc.challonge.com/vhfqet4z