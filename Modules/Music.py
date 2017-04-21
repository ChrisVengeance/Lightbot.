import discord
from discord.ext import commands
import asyncio
import random
import datetime
import json
from Util.FilePrinter import youtube
from Util.FilePrinter import nextSong


MIN_VIEWS = 8000
MAX_PERCENT_DISLIKE = 0.25
MAX_LENGTH = 1200
MAX_SONGS_SHOWN = 10
MAXLOOPS = 5
VERSION = "0.4.3"

class MusicPlayer:

	def isStaff(self, ctx):
	    for role in ctx.message.author.roles:
	        if role.name == "Staff":
	            return True
	    return False

	def __init__(self, bot):
		with open('Playlists.json', 'r') as f:
			self.playList = json.load(f)
		self.bot = bot
		self.voice = None
		self.player = None
		self.queue = []
		self.radio = False
		self.skipList = []
		self.requester = None
		self.bot.loop.create_task(self.useQueue())
		self.previousLooper = "0"

	@commands.command()
	async def music(self):
		'Returns the current status of the Music Bot'
		await self.bot.say("Version: {}\nQueue Length: {}\nRadio Mode: {}\nConnected Channel: {}\nSong Playing: {}".format(VERSION, len(self.queue), self.radio, self.voice.channel.name, self.player.title))

	@commands.command()
	async def songs(self):
		'Prints the songs in the queue'
		ret = ""
		if len(self.queue) != 0: #There is something in the Queue
			count = 1
			if len(self.queue) <= MAX_SONGS_SHOWN: #There are less than [MAX_SONGS_SHOWN] in the Queue
				await self.bot.say("**The Following songs are in the Queue**")
				for song in self.queue:
					ret += str(count) + ". " + song[0].title + " **" + song[1] + "**\n\t<" + song[0].url + ">\n"
					count+=1
			else:
				await self.bot.say("**The Following songs are in the Queue, plus [{}] more**".format(len(self.queue) - MAX_SONGS_SHOWN))
				for x in range(0,MAX_SONGS_SHOWN,1):
					ret += str(count) + ". " + self.queue[x][0].title + " **" + self.queue[x][1] + "**\n\t<" + self.queue[x][0].url + ">\n"
					count+=1
		else:
			await self.bot.say("Queue is Empty")
			return
		ret += "Total Time is {}".format(str(datetime.timedelta(seconds = self.totalTime(self.queue))))
		await self.bot.say(ret)


	def totalTime(self, queue):
		time = 0
		for elem in queue:
			time += elem[0].duration
		return time

	@commands.command()
	async def shuffle(self):
		'Shuffles the songs in the Queue'
		await self.bot.say("Shuffling songs...")
		random.shuffle(self.queue)

	@commands.command(pass_context = True)
	async def remove(self, ctx, number : int):
		'removes a song from a queue by index'
		if(len(self.queue) < number):
			await self.bot.say("The Queue isnt that long!")
			return
		currentName = self.queue[number - 1][1]
		if currentName == ctx.message.author.name or ctx.message.author.id == "226028320104382464" or currentName == "Radio":
			current = self.queue.pop(number - 1)[0]
			if not current.is_done:
				current.start()
			current.stop()
			await self.bot.say("Removed: " + current.title)
		else:
			await self.bot.say("You must be the requester of the song to remove it from queue!")

	@commands.command(hidden = True, pass_context = True)
	async def forceplay(self,ctx, link : str):
		if(ctx.message.author.id != "226028320104382464"):
			return
		self.requester = ctx.message.author.name
		current = await self.voice.create_ytdl_player(link)
		if(self.player != None):
			self.player.stop()
		self.player = current
		self.player.start()
		self.skipList = []

	@commands.command(pass_context = True)
	async def loop(self, ctx, num = 1):
		'Plays the current song again'
		ID = ctx.message.author.id
		if ID not in [x.id for x in self.voice.channel.voice_members]:
			await self.bot.say("You need to be in the voice channel!")
			return
		if(num > MAXLOOPS and ctx.message.author.id != "226028320104382464"):
			await self.bot.say("Can not loop that many times!")
			return
		if(self.previousLooper == ctx.message.author.id and len(self.voice.channel.voice_members) > 2 and ctx.message.author.id != "134441036905840640"):
			await self.bot.say("You can not loop more than once in a row! Please wait for someone else to loop a song.")
			return
		self.previousLooper = ctx.message.author.id

		current = await self.voice.create_ytdl_player(self.player.url)
		final = (current, ctx.message.author.name)
		for x in range(0,num,1):
			self.queue.insert(0, final)
		await self.bot.say("Added '*{}*' **{}** more times".format(self.player.title, num))

	@commands.command()
	async def playlists(self):
		'Shows all the current playlists'
		with open('Playlists.json', 'r') as f:
			self.playList = json.load(f)
		Names = []
		for name, songs in self.playList.items():
			if(songs != None and name != None):
				Names.append(name + "[" + str(len(songs)) + "]")
		await self.bot.say(", ".join(Names))

	@commands.command(pass_context = True)
	async def youtube(self,ctx, * links : str):
		'Adds a Song for the Bot to Play'
		ID = ctx.message.author.id
		if ID not in [x.id for x in self.voice.channel.voice_members]:
			await self.bot.say("You need to be in the voice channel!")
			return

		if(self.voice == None):
			await self.bot.say("I am not connected to a Voice Chat!")
			return

		for link in links:
			if("www.youtube.com/watch?v" not in link and "https://youtu.be/" not in link):
				await self.bot.say("Not a Valid Link, Please only use URLs from youtube.com")
				break
			try:
				current = await self.voice.create_ytdl_player(link)
			except Exception as e:
				self.bot.say(e)
				break
			if(current.views < MIN_VIEWS):
				await self.bot.say("Sorry, that video has too little views to be Trustworthy. Needs [{}] but has [{}]".format(format(MIN_VIEWS, ",d"), format(current.views, ",d")))
				current.start()
				current.stop()
				break
			elif(current.dislikes / (current.dislikes + current.likes) > MAX_PERCENT_DISLIKE):
				await self.bot.say("Sorry, too many people dislike that video. Needs to be below [{}%] but was [{}%]".format(MAX_PERCENT_DISLIKE * 100, round(current.dislikes / (current.dislikes + current.likes) * 100,2)))
				current.start()
				current.stop()
				break
			elif(current.duration > MAX_LENGTH):
				await self.bot.say("Sorry, that video is too long, it must be under [{}] minutes!".format(MAX_LENGTH/60))
				current.start()
				current.stop()
				break
			await self.bot.say("Added {} to the queue".format(current.title))
			self.queue.append((current, ctx.message.author.name))
			print("Added Song to Queue")
			#await asyncio.sleep(3)

		# self.player.start()
		#print(player.views, player.likes, player.dislikes)
	@commands.command(pass_context = True)
	async def search(self, ctx, * Pinput : str):
		'Searches for a song'
		ID = ctx.message.author.id
		if ID not in [x.id for x in self.voice.channel.voice_members]:
			await self.bot.say("You need to be in the voice channel!")
			return
		if(self.voice == None):
			await self.bot.say("I am not connected to a Voice Chat!")
			return

		count = 0
		link = youtube("+".join(Pinput), count)
		current = await self.voice.create_ytdl_player(link)
		while(current == None or current.views < MIN_VIEWS or current.dislikes / (current.dislikes + current.likes) > MAX_PERCENT_DISLIKE or current.duration > MAX_LENGTH):
			current.start()
			current.stop()
			link = youtube("+".join(Pinput), count)
			current = await self.voice.create_ytdl_player(link)
			count += 1
		await self.bot.say("Added {} to the queue".format(current.title))
		await self.bot.say(link)
		self.queue.append((current, ctx.message.author.name))

	async def useQueue(self):
		await self.bot.wait_until_ready()
		print("Running Queue")
		while not self.bot.is_closed:
			if len(self.queue) != 0:
				if self.player is None:
					print("Starting to play music")
					song = self.queue.pop(0)
					self.requester = song[1]
					await self.playSong(song[0])
				if self.player.is_playing() is False:
					print("Playing next song...")
					song = self.queue.pop(0)
					self.requester = song[1]
					await self.playSong(song[0])
			else:
				if(self.radio and self.player is not None):
					link = nextSong(self.player.url)
					current = await self.voice.create_ytdl_player(link)
					count = 0
					while(current == None or current.views < MIN_VIEWS or current.dislikes / (current.dislikes + current.likes) > MAX_PERCENT_DISLIKE or current.duration > MAX_LENGTH):
						current.start()
						current.stop()
						link = nextSong(self.player.url, count)
						current = await self.voice.create_ytdl_player(link)
						while(current.likes == None):
							current.start()
							current.stop()
							link = nextSong(self.player.url, count)
							current = await self.voice.create_ytdl_player(link)
							count += 1						
						count += 1
					self.queue.append((current, "Radio"))
			await asyncio.sleep(1)
		print("Finished Queue :(")


	async def playSong(self, current):
		if(self.player != None):
			self.player.stop()
		link = current.url
		if not current.is_done():
			current.start()
		current.stop()
		self.player = await self.voice.create_ytdl_player(link)
		self.player.start()
		self.player.volume = 0.6
		self.skipList = []


	@commands.command(pass_context = True)
	async def join(self,ctx):
		'Joins the Voice channel you are currently in'
		#self.voice == self.bot.voice_client_in(ctx.message.server)
		if self.voice != None:
			await self.bot.say("Sorry, I'm already connected to a channel in server {}".format(self.voice.server))
			return
		channel = ctx.message.author.voice_channel
		if channel is None:
			await self.bot.say("You are not connected to a voice channel!")
		else:
			try:
				self.voice = await self.bot.join_voice_channel(channel)
			except:
				self.voice = ctx.message.server.voice_client

	@commands.command()
	async def Radio(self):
		'Toggles Radio Mode'
		self.radio = not self.radio
		await self.bot.say("Radio Mode: {}".format(self.radio))

	@commands.command()
	async def leave(self):
		'Leaves the Join chat'
		for x in self.queue:
			if not x[0].is_done:
				x[0].start()
			x[0].stop()
		self.queue = []
		await self.voice.disconnect()
		self.voice = None

	@commands.command(pass_context=True, hidden=True)
	async def musicdebug(self, ctx, *, code : str):
	    IDs = ["226028320104382464", "126122455248011265"]
	    if(ctx.message.author.id not in IDs):
	        return
	    """Evaluates code."""
	    code = code.strip('` ')
	    python = '```py\n{}\n```'
	    result = None

	    try:
	        result = eval(code)
	    except Exception as e:
	        await self.bot.say(python.format(type(e).__name__ + ': ' + str(e)))
	        return

	    if asyncio.iscoroutine(result):
	        result = await result

	    await self.bot.say(python.format(result))

	@commands.command()
	async def clear(self):
		'Clears the Queue'
		for x in self.queue:
			try:
				x[0].start()
			except:
				print("It no work")
			x[0].stop()
			self.queue.remove(x)
		await self.bot.say("Cleared Queue!")

	@commands.command()
	async def song(self):
		'Returns information about the current playing song'
		try:
			await self.bot.say("**Name**: " + str(self.player.title) + "\n" + 
			"**Requester**: " + str(self.requester) + "\n" +
			"**URL**: <" + str(self.player.url) + ">\n" +  
			"```py\nTime: " + str(datetime.timedelta(seconds = self.player.duration)) + "\n" +
			"Views: " + str(format(self.player.views, ',d')) + "\n" +
			"Likes: " + str(format(self.player.likes, ',d')) + ", " + str(round(self.player.likes/(self.player.likes + self.player.dislikes) * 100, 2)) + "%\n" + 
			"Dislikes: " + str(format(self.player.dislikes, ',d')) + ", " + str(round(self.player.dislikes/(self.player.likes + self.player.dislikes) * 100, 2)) + "%\n" +
			"Skips: " + str(len(self.skipList)) + "/" + str(int(2*(len(self.voice.channel.voice_members)-1)/3)) + "```"
			)
		except Exception as e:
			await self.bot.say("No Song Playing, [{}]".format(e))

	@commands.command()
	async def desc(self):
		'Decription of the Current playing song'
		await self.bot.say("Current Song Description:\n{}".format(self.player.description[:1000]))

	@commands.command(pass_context = True)
	async def skip(self, ctx):
		'Skips the Current song'
		ID = ctx.message.author.id

		# Only people in the channel can mute
		if ID not in [x.id for x in self.voice.channel.voice_members]:
			await self.bot.say("You need to be in the voice channel!")
			return

		# Requester wants to skip
		if ctx.message.author.name == self.requester:
			await self.bot.say("Skipping {} by request of the requester".format(self.player.title))
			self.player.stop()
			self.skipList = []
			return

		# Its a Radio Song
		if self.requester == "Radio":
			await self.bot.say("Skipping {} by request (Radio Song)".format(self.player.title))
			self.player.stop()
			self.skipList = []
			return

		NeededToSkip = int(2*(len(self.voice.channel.voice_members)-1)/3)

		# Add a new `Skipper` to the list
		if ID not in self.skipList:
			self.skipList.append(ID)
			await self.bot.say("{}/{} votes to skip".format(len(self.skipList), NeededToSkip))
		# If Enough votes, skip the song
		if len(self.skipList) >= NeededToSkip:
			await self.bot.say("Skipping {} by popular vote.".format(self.player.title))
			self.player.stop()
			self.skipList = []
	# Playlist Stuff

	@commands.command(pass_context = True)
	async def playlist(self, ctx, *names : str):
		'Adds songs from a predefined playlist to the songs list'
		with open('Playlists.json', 'r') as f:
			self.playlist = json.load(f)
		for name in names:
			random.shuffle(self.playList[name])
			for song in self.playList[name]:
				try:
					current = await self.voice.create_ytdl_player(song)
					self.queue.append((current, ctx.message.author.name))
				except Exception as e:
					print("Could Not Add a Song... Skipping it: <{}>".format(e))

		await self.bot.say("Finished Adding songs from playlist(s)")

	@commands.command()
	async def makeplaylist(self, name, *links : str):
		'Makes a custom playlist for the bot to save'
		with open('Playlists.json', 'r') as f:
			self.playList = json.load(f)
		if(name in self.playList.keys()):
			await self.bot.say("Playlist already exists")
			return
		self.playList[name] = list(links)
		with open('Playlists.json', 'w') as f:
			json.dump(self.playList, f)
		await self.bot.say("Created Playlist {} with {} songs".format(name, len(list(links))))

	@commands.command()
	async def viewplaylist(self, name):
		'Views the songs of a playlists'
		with open('Playlists.json', 'r') as f:
			self.playList = json.load(f)
		if(name not in self.playList.keys()):
			await self.bot.say("Playlist does not exists")
			return
		try:
			songNames = await self.getNames(self.playList[name])
		except Exception as e:
			await self.bot.say(e)
			return
		await self.bot.say("\n".join(songNames))

	async def getNames(self, names):
		cleanNames = []
		for name in names:
			try:
				song = await self.voice.create_ytdl_player(name)
				cleanNames.append(song.title + " <{}>".format(song.url))
				song.start()
				song.stop()
			except Exception as e:
				print("{}\nBAD SONG IN A PLAYLIST".format(e))
		return cleanNames


	@commands.command()
	async def extendplaylist(self, name, *links : str):
		'Extends a custom playlist'
		with open('Playlists.json', 'r') as f:
			self.playList = json.load(f)
		if(name not in self.playList.keys()):
			await self.bot.say("Playlist does not exists")
			return
		self.playList[name].extend(list(links))
		with open('Playlists.json', 'w') as f:
			json.dump(self.playList, f)

	@commands.command(hidden = True)
	async def removeplaylist(self, name):
		'Removes a custom playlist'
		with open('Playlists.json', 'r') as f:
			self.playList = json.load(f)
		if(name not in self.playList.keys()):
			await self.bot.say("Playlist does not exists")
			return			
		del self.playList[name]
		with open('Playlists.json', 'w') as f:
			json.dump(self.playList, f)
		await self.bot.say("Removed {}".format(name))



def setup(bot):
	bot.add_cog(MusicPlayer(bot))

	
