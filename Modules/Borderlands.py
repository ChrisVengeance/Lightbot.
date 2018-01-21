import discord
from discord.ext import commands 
import asyncio

class Borderlands:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(hidden = True)
	async def Harold(self):
		await self.bot.say("The Unkempt Harold Can Be Farmed From Savage Lee Or Torgue Vendors From the Campaign of Carnage DLC")


	@commands.command(hidden = True)
	async def ClassMods(self):
		await self.bot.say("All Legendary ClassMods Can be Farmed From Tubby's or From the Mercenary Day DLC Chests After Killing Tinder Snowflake")


	@commands.command(hidden = True)
	async def StormFront(self):
		await self.bot.say("The StormFront Legendary Grenade can be Farmed From The Splinter Group After completing the Splinter Group Quest given by tannis in sanctuary")

	@commands.command(hidden = True)
	async def ChainLightning(self):
		await self.bot.say("The Chain Lightning Legendary Grenade Can Be Farmed From Any Variation of BADASS Sorcerers in the Tiny Tina DLC (This Includes Handsome Sorcerer)")

	@commands.command(hidden = True)
	async def Wiki(self):
		await self.bot.say("http://borderlands.wikia.com/wiki/Borderlands_Wiki")

	@commands.command(hidden = True)
	async def Bitch(self):
		await self.bot.say("This Legendary SMG is mainly found by farming the BNK-3R after the main story quest where angels fear to tread is completed")

	@commands.command(hidden = True)
	async def ConferenceCall(self):
		await self.bot.say("This Legendary Shotgun can be found from either farming the Warrior or from the Handsome Sorcerer")

	@commands.command(hidden = True)
	async def Sham(self):
		await self.bot.say("The Sham Legendary Shield is Obtained from the BNK-3R")

	@commands.command(hidden = True)
	async def Unique(self):
		await self.bot.say("Check here for Specific Uniques, http://borderlands.wikia.com/wiki/Category:Unique")

	@commands.command(hidden = True)
	async def BLHelp(self):
		await self.bot.say("Here's a list of Borderlands Commands!,Wiki,ChainLightning,Harold,Sham,Bitch,ClassMods,StormFront,ConferenceCall,Unique, All Commands Start with .")


	@commands.command(hidden = True)
	async def FusterCluck(self):
		await self.bot.say("The FusterCluck Is a Unique MIRV Grenade Mod, Can Only Be Obtained By Completeing The Mission (The Pretty Good Train Robbery) Located In Tundra Express. HOWEVER i wouldn't recommend using this grenade mod long term as it's not very good")

























def setup(bot):
    bot.add_cog(Borderlands(bot))
