import discord
from discord.ext import commands
import asyncio

class Warframe:
	def __init__(self, bot):
		self.bot = bot


@commands.command(hidden = True)
async def Ash(self):
	await self.bot.say("The Ash warframe components can be dropped from Manics both Grineer and Drekar and the blueprint can be purchased from the market")

@commands.command(hidden = True)
async def Nekros(self):
	await self.bot.say("The Nekros warframe components are dropped by Lephantis in the orokin derelict assassinate mission, while the main blueprint is purchased from the market for 100,000 credits")

@commands.command(hidden = True)
async def Mesa(self):
	await self.bot.say("The Mesa components can be obtained from Mutalist Alad V on Eris after crafting the blueprint")


@commands.command(hidden = True)
async def Ship(self):
	await self.bot.say("each of the different ship components can be found in rare loot containers mostly found in the derelict but can be found in any mission")


@commands.command(hidden = True)
async def Platinum(self):
	await self.bot.say("Platinum can be bought from the playstation store for various prices")


























































































































































































def setup(bot):

	bot.add_cog(Warframe(bot))
