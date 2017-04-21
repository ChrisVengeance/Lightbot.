import discord
import time
from discord.ext import commands
from subprocess import Popen
import asyncio

EXTENTIONS = ['Modules.StaffCmds', 'Modules.Interaction', 'Modules.Music', 'Modules.Games']

def isStaff(ctx):
    for role in ctx.message.author.roles:
        if role.name == "Staff":
            return True
    return True

class StaffCmds:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context = True)
	async def mute(self, ctx, member : str):
	    if not isStaff(ctx):
	        return
	    overwrite = discord.PermissionOverwrite()
	    overwrite.send_messages = False
	    try:
	    	await self.bot.edit_channel_permissions(ctx.message.channel, ctx.message.server.get_member_named(member), overwrite);
	    except Exception as e:
	    	await self.bot.say("Something went Wrong: {}".format(type(e).__name__))
	    	return
	    await self.bot.say("Muted {}".format(member))

	@commands.command(pass_context = True)
	async def unmute(self, ctx, member : str):
	    if not isStaff(ctx):
	        return
	    overwrite = discord.PermissionOverwrite()
	    overwrite.send_messages = True
	    try:
	    	await self.bot.edit_channel_permissions(ctx.message.channel, ctx.message.server.get_member_named(member), overwrite);
	    except Exception as e:
	    	await self.bot.say("Something went Wrong: {}".format(type(e).__name__))
	    	return

	    await self.bot.say("Unmuted {}".format(member))

	@commands.command(pass_context = True)
	async def tempmute(self, ctx, member : str, timeToMute : int):
	    if not isStaff(ctx):
	        return
	    overwrite = discord.PermissionOverwrite()
	    overwrite.send_messages = False
	    try:
	    	await self.bot.edit_channel_permissions(ctx.message.channel, ctx.message.server.get_member_named(member), overwrite);
	    except Exception as e:
	   		await self.bot.say("Something went Wrong: {}".format(type(e).__name__))
	    await self.bot.say("Muted {}".format(member))

	    await asyncio.sleep(timeToMute)

	    overwrite = discord.PermissionOverwrite()
	    overwrite.send_messages = True
	    try:
	    	await self.bot.edit_channel_permissions(ctx.message.channel, ctx.message.server.get_member_named(member), overwrite);
	    except Exception as e:
	    	await self.bot.say("Something went Wrong: {}".format(type(e).__name__))
	    await self.bot.say("Unmuted {}".format(member))

	@commands.command(pass_context = True)
	async def mutelist(self, ctx):
		channel = ctx.message.channel
		mutedList = []
		for x in channel.server.members:
			if(x.permissions_in(channel).send_messages == False):
				mutedList.append(x.name)
		if len(mutedList) != 0:
			await self.bot.say("Muted Players in this Channel...")
			await self.bot.say(", ".join(mutedList))
		else:
			await self.bot.say("No One is Muted in this Channel!")

	@commands.command(pass_context = True)
	async def unmuteall(self,ctx):
	    'Unmutes ALL muted players'
	    if not isStaff(ctx):
	        return
	    channel = ctx.message.channel
	    mutedList = []
	    for x in channel.server.members:
	        if(x.permissions_in(channel).send_messages == False):
	            mutedList.append(x.name)

	    overwrite = discord.PermissionOverwrite()
	    overwrite.send_messages = True
	    try:
	        for player in mutedList:
	            await self.bot.edit_channel_permissions(ctx.message.channel, ctx.message.server.get_member_named(player), overwrite);
	    except Exception as e:
	        await self.bot.say("Something went Wrong")
	        return
	    await self.bot.say("Unmuting all players...")

	@commands.command(pass_context = True, hidden = True)
	async def cmd(self,ctx, command : str):
	    '''Returns the Given W/E Cmd (Only Usable by Wertfuzzy77)'''
	    if not isStaff(ctx):
	        return
	    else:
	        try:
	            await self.bot.say(Commands[command])
	        except Exception:
	            await self.bot.say("Sorry, Couldn't Find that Command.")

	@commands.command(pass_context = True, name='reload', hidden=True)
	async def reload(self, ctx):
	    """Reloads all of the modules."""
	    if ctx.message.author.id is not 226028320104382464:
	    	return
	    try:
	        for module in EXTENTIONS:
	            self.bot.unload_extension(module)
	            self.bot.load_extension(module)
	    except Exception as e:
	        await self.bot.say('Something went wrong :(')
	        await self.bot.say('{}: {}'.format(type(e).__name__, e))
	    else:
	        await self.bot.say('Reloaded all Modules')

def setup(bot):
	bot.add_cog(StaffCmds(bot))