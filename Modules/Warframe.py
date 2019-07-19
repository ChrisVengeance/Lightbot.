import discord
from discord.ext import commands
import asyncio

class League:
	def __init__(self, bot):
		self.bot = bot


@commands.command(pass_context = True)
async def DariusItems(self, ctx):
	Embed = discord.Embed(title="DariusItemList", colour=0x4AA9D6)
	Conqueror = ["Trinity Force", 'Spirit Visage', 'Steraks Gage', 'Guardian Angel', 'Deadmans Plate']
	AfterShock = ["Spirit Visage", 'Black Cleaver', 'Guardian Angel', 'Deadmans Plate', 'Steraks Gage']
	Situationals = ["Randuins Omen", 'Thorn Mail', 'Righteous Glory', 'Adaptive Helm']
	StaterItems = ["Corrupting Potion", 'Health Potion', 'Ninja Tabi', 'Merc Treads', 'Dorans Shield']
	Misc = ["Control Ward"]
	Embed.add_field(name = "Conqueror", value = "{}".format(", ".join(Conqueror)))
	Embed.add_field(name = "AfterShock", value = "{}".format(", ".join(AfterShock)))
	Embed.add_field(name = "Situationals", value ="{}".format(", ".join(Situationals)))
	Embed.add_field(name = "StarterItems", value = "{}".format(" ,".join(StarterItems)))
	Embed.add_field(name = "Misc", value = "{}".formant(", ".join(Misc)))
	await self.bot.send_message(ctx.message.channel, embed = Embed)













































































































































































def setup(bot):

	bot.add_cog(League(bot))
