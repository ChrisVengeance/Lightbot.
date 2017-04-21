import discord
from discord.ext import commands
import asyncio
from collections import defaultdict
import time
import random
import operator
import time
import json
import math

from Util.PokemonJson import *

COOLDOWN = 90
TCOOLDOWN = 1800
NUM_MOVES = 8

class Games:
	def __init__(self, bot):
		self.bot = bot
		self.inGame = False
		self.LEVEL = 0 # Scales the HP of the Boss
		self.boss = Boss(self.LEVEL)
		self.players = {}
		self.AUTO_RESPAWN = False
		self.training = {}
		

	@commands.command(pass_context = True)
	async def trivia(self, ctx, num : int  = 10):
	    if self.inGame:
	        await self.bot.say("Already playing a game, wait for that one to finish.")
	        return
	    self.inGame = True
	    trivia_timeout = 30
	    current_channel = ctx.message.channel.id
	    winners = defaultdict(int)

	    async def ask(final_answer:list):
	      """ Condensed methodology for asking questions in any question mode """
	      await self.bot.say("""You have Thirty seconds to submit an answer using ;ans [Your Answer]...
	        \n\n**Note:** If you know it and want to save it for the end, be wary that it may not recognize some answers if multiple are simultaneous!
	        """)
	      final_answer_f = list(map(lambda x: x.lower().replace(" ", ""), final_answer))
	      print(final_answer_f)

	      answers = {}
	      timeout = time.time() + (trivia_timeout - 15)
	      while time.time() < timeout:
	        ans = await self.bot.wait_for_message(timeout=1.0)
	        if ans and ans.channel.id == current_channel and ans.author.id != '167123959031005186' and ans.content.startswith(";ans"):
	            answers[ans.author.name] = ans.content.replace(";ans ", "")
	            try:
	                await self.bot.delete_message(ans)
	            except Exception:
	                traceback.print_exc()
	                continue



	      await self.bot.say('Currently received an answer from: {}\n\nYou have ten more seconds to respond.'.format(', '.join(answers)))

	      timeout = time.time() + 15
	      while time.time() < timeout:
	        ans = await self.bot.wait_for_message(timeout=1.0)
	        if ans and ans.channel.id == current_channel and ans.author.id != '167123959031005186' and ans.content.startswith(";ans"):
	            answers[ans.author.name] = ans.content.replace(";ans ", "")
	            try:
	                await self.bot.delete_message(ans)
	            except Exception:
	                traceback.print_exc()
	                continue


	      final_message = "**Here are the results**:\n"
	      for name,resp in answers.items():
	        final_message += "{} guessed `{}` ... ".format(name, resp)
	        if resp.lower().replace(" ", "") in final_answer_f:
	          winners[name] += 1
	          final_message += "**CORRECT!**\n"
	        else:
	          final_message += "*Incorrect*\n"

	      final_message += '\nThe answer was: **{}**\n'.format(final_answer)
	      await self.bot.say(final_message + '\n')

	    GameType = random.choice(["Text", "HiddenAbility", "Question", "Mixed"])
	    GameType = "Text"
	    await self.bot.say("Lets play the {} game".format(GameType))
	    for i in range(1, num + 1 if num>=1 else 11):
	        await self.bot.say("Next Question in 5 Seconds")
	        timeout = time.time() + 5
	        while time.time() < timeout:
	            ans = await self.bot.wait_for_message(timeout=1.0)

	        pokemon = getName(getRandomID())
	        await self.bot.say("Question {}".format(i))
	        if GameType == "Mixed":
	            my_list = ["Text"] * 1 + ["HiddenAbility"] * 2 + ["Question"] * 3
	            choose = random.choice(my_list)
	        else:
	            choose = GameType

	        if(choose == "Text"):
	            text = getPokemonFlavorText(pokemon)
	            await self.bot.say("Which Pokemon is This?\n**{}**".format(text))
	            await ask([pokemon])

	    winners_message = "**Current winners:**\n"
	    for q in sorted(winners, key=winners.get, reverse=True):
	        winners_message += '{}: *{}* correct\n'.format(q, winners[q])
	    await self.bot.say(winners_message + '\n')
	    self.inGame = False

	@commands.command(pass_context = True)
	async def pokebattle(self, ctx, moves = ""):
		'Fights a Pokemon Boss using a combination of 10 total moves 8 times.'
		if ctx.message.author.id in list(self.players.keys()):
			if self.players[ctx.message.author.id] + COOLDOWN > time.time():
				await self.bot.say("Please wait {} seconds before you can fight the boss again.".format(round(self.players[ctx.message.author.id] + COOLDOWN - time.time()), 0))
				return
		moves = moves.upper()
		if moves == "" or len(moves) is not NUM_MOVES:
			await self.bot.say("Please use a Combination of **{}** Types to Fight the Boss: (**N**)ormal, (**F**)ire, (**W**)ater, (**G**)rass, (**P**)oison, (**D**)ragon, (**S**)teel, (**E**)lectric, (**B**)ug, or (**I**)ce.\n Ex 'GSEBI' or 'DPGDB'".format(NUM_MOVES))
			return
		for x in moves:
			if x not in ["N","F","W","G","P","D","S","E","B","I"]:
				await self.bot.say("Please use a Combination of **{}** Types to Fight the Boss: (**N**)ormal, (**F**)ire, (**W**)ater, (**G**)rass, (**P**)oison, (**D**)ragon, (**S**)teel, (**E**)lectric, (**B**)ug, or (**I**)ce.\n Ex 'GSEBI' or 'DPGDB'".format(NUM_MOVES))
				return

		if self.boss.isDefeated and self.AUTO_RESPAWN:
			self.boss = Boss(self.LEVEL)
		elif self.boss.isDefeated and not self.AUTO_RESPAWN:
			await self.bot.say("The Boss has been Defeated! Please check ;pokeboss for stats.")
			return

		if not self.boss.hasBeenRevealed:
			await self.bot.say("A Level {} Boss **{}** has appeared!\nIt has {} Health.".format(self.LEVEL, self.boss.Name, self.boss.Health))

			f = open('BossImage.jpg','wb')
			f.write(requests.get(self.boss.Image).content)
			f.close()

			await self.bot.send_file(ctx.message.channel, "BossImage.jpg")
			self.boss.hasBeenRevealed = True
		else:
			await self.bot.say("Level {} Boss **{}** has {} health left.".format(self.LEVEL, self.boss.Name, self.boss.Health))
			await self.bot.send_file(ctx.message.channel, "BossImage.jpg")
		correctOnes = [self.boss.combination[x] == moves[x] for x in range(0, NUM_MOVES, 1)]

		Pinput = [":regional_indicator_{}:".format(value.lower()) for value in moves]
		output = [":white_check_mark:" if value else ":x:" for value in correctOnes]
		await self.bot.say(" ".join(Pinput) + "\n" + " ".join(output))
		self.boss.lastUsedCombo = " ".join(Pinput) + "\n" + " ".join(output)
		# Calculate Damage done, Varies from 75% - 125%

		with open('Players.json', 'r') as f:
			ALLPLAYERS = json.load(f)
		try:
			pre = ALLPLAYERS[ctx.message.author.id]
			player = await self.checkLevel(pre)
			if pre['Level'] is not player['Level']:
				await self.bot.say("You Have Leveled up from {} to {}".format(pre['Level'], player['Level']))
		except:
			ALLPLAYERS[ctx.message.author.id] = {"Name" : ctx.message.author.name, "Level": 0, "XP": 0, "Large_Damage" : 0, "Takedowns" : 0}	
			player = ALLPLAYERS[ctx.message.author.id]

		with open('Players.json', 'w') as f:
			json.dump(ALLPLAYERS, f)

		dmg = player['Level']
		if dmg == 0:
			dmg = 1

		Total_Damage = [dmg * 1.1 if value else 0 for value in correctOnes]
		Total_Damage = sum(Total_Damage)
		if random.random() < 0.10:
			await self.bot.say("Its a Critical Strike")
			Total_Damage = Total_Damage * 2
		if correctOnes.count(True) == NUM_MOVES - 1:
			await self.bot.say("Its Super Effective! The Boss has switched 1/4 of the Super Effective Moves!")
			Total_Damage = Total_Damage * NUM_MOVES * 1.5
			for x in range (0, int(NUM_MOVES/4), 1):
				self.boss.change1()
		elif correctOnes.count(True) == NUM_MOVES:
			await self.bot.say("Its a Perfect Combo. The Boss has switched 1/2 of the Super Effective Moves!")
			Total_Damage = Total_Damage * NUM_MOVES * 3
			for x in range (0, int(NUM_MOVES/2), 1):
				self.boss.change1()
		elif correctOnes.count(True) > NUM_MOVES / 2:
			await self.bot.say("Its Sort-Of Effective")
			Total_Damage = Total_Damage * 2

		if player['Level'] > self.LEVEL * 2 and self.LEVEL > 0:
			Total_Damage = Total_Damage * self.LEVEL / player["Level"]
			await self.bot.say("*Low level boss penalty...*")

		if self.boss.summoner == ctx.message.author.name:
			await self.bot.say("Rival Bonus!")
			Total_Damage = Total_Damage * 1.25
		if Total_Damage is not 0:
			Total_Damage = int(Total_Damage * random.randrange(75, 125, 5) / 100 + 1)

		await self.dealDamage(ctx.message.author, Total_Damage)
		await self.bot.say("Your moves did **{}** damage".format(Total_Damage))


		self.boss.Health = self.boss.Health - Total_Damage

		await self.giveXP(ctx.message.author, int(Total_Damage/12))
		
		try: 
			self.boss.Damage[ctx.message.author] = self.boss.Damage[ctx.message.author] + Total_Damage
		except:
			self.boss.Damage[ctx.message.author] = Total_Damage



		if self.boss.Health <= 0:
			await self.takeDown(ctx.message.author)
			await self.bot.say("Level {} Boss **{}** has been defeated!".format(self.LEVEL, self.boss.Name))
			sorted_Damage = sorted(self.boss.Damage.items(), key=operator.itemgetter(1), reverse=True)
			try:
				await self.bot.say("Most Damage by **{}** with **{}** damage".format(sorted_Damage[0][0].name, sorted_Damage[0][1]))
			except:
				await self.bot.say("Most Damage by *UNKNOWN* with **{}** damage".format(sorted_Damage[0][1]))
			if len(sorted_Damage) >= 2:
				try:
					await self.bot.say("2nd most Damage by *{}* with *{}* damage".format(sorted_Damage[1][0].name, sorted_Damage[1][1]))
				except:
					await self.bot.say("Most Damage by *UNKNOWN* with **{}** damage".format(sorted_Damage[1][1]))
			if len(sorted_Damage) >= 3:
				try:
					await self.bot.say("3rd most Damage by *{}* with *{}* damage".format(sorted_Damage[2][0].name, sorted_Damage[2][1]))
				except:
					await self.bot.say("Most Damage by *UNKNOWN* with **{}** damage".format(sorted_Damage[2][1]))
			if len(sorted_Damage) >= 4:
				await self.bot.say("Assisted by {}".format(", ".join([sorted_Damage[x][0].name for x in range(3, len(sorted_Damage), 1)])))
			self.boss.isDefeated = True
			# XP

			await self.giveXP(sorted_Damage[0][0], int(self.boss.StartingHealth*.10) + int(self.boss.Damage[sorted_Damage[0][0]]/2) + 1)
			if len(sorted_Damage) >= 2:
				await self.giveXP(sorted_Damage[1][0], int(self.boss.StartingHealth*.05) + int(self.boss.Damage[sorted_Damage[1][0]]/3) + 1)
			if len(sorted_Damage) >= 3:
				await self.giveXP(sorted_Damage[2][0], int(self.boss.StartingHealth*.03) + int(self.boss.Damage[sorted_Damage[2][0]]/5) + 1)
			if len(sorted_Damage) >= 4:
				members = [sorted_Damage[x][0] for x in range(3, len(sorted_Damage), 1)]
				for member in members:
					await self.giveXP(member, int(self.boss.StartingHealth * 0.01) + 1)

			self.players = {}
		else:
			await self.bot.say("Level {} Boss **{}** has {} health left.".format(self.LEVEL, self.boss.Name, self.boss.Health))
			self.players[ctx.message.author.id] = time.time()

	async def dealDamage(self, member, damage):
		with open('Players.json', 'r') as f:
			ALLPLAYERS = json.load(f)
		try:
			player = await self.checkLevel(ALLPLAYERS[member.id])
		except:
			print("NEW PLAYER: {}".format(ctx.message.author.name))
			ALLPLAYERS[member.id] = {"Name" : member.name, "Level": 0, "XP": 0, "Large_Damage" : 0, "Takedowns" : 0}	
			player = ALLPLAYERS[member.id]
		if(player['Large_Damage'] < damage):
			ALLPLAYERS[member.id]['Large_Damage'] = damage
		with open('Players.json', 'w') as f:
			json.dump(ALLPLAYERS, f)

	async def takeDown(self, member):
		with open('Players.json', 'r') as f:
			ALLPLAYERS = json.load(f)
		try:
			player = await self.checkLevel(ALLPLAYERS[member.id])
		except:
			print("NEW PLAYER: {}".format(ctx.message.author.name))
			ALLPLAYERS[member.id] = {"Name" : member.name, "Level": 0, "XP": 0, "Large_Damage" : 0, "Takedowns" : 0}	
			player = ALLPLAYERS[member.id]
		ALLPLAYERS[member.id]['Takedowns'] += 1
		with open('Players.json', 'w') as f:
			json.dump(ALLPLAYERS, f)
		
	@commands.command(pass_context = True)
	async def summon(self, ctx, level : int = 0):
		'Summons a Boss of your Level or a Level below yours'
		if not self.boss.isDefeated:
			await self.bot.say("Please wait for the current boss to be defeated before you summon a new one!")
			return
		with open('Players.json', 'r') as f:
			ALLPLAYERS = json.load(f)
		try:
			player = await self.checkLevel(ALLPLAYERS[ctx.message.author.id])
		except:
			ALLPLAYERS[ctx.message.author.id] = {"Name" : ctx.message.author.name, "Level": 0, "XP": 0, "Large_Damage" : 0, "Takedowns" : 0}
			player = ALLPLAYERS[ctx.message.author.id]

		if level == 0 and player['Level'] is not 0:
			await self.bot.say("Please summon a boss from level {0} to {1} (Ex. `;summon {1}`)".format(int(player['Level']/2), player['Level']))
			return
		if level < int(player['Level'] / 2) and player['Level'] is not 0:
			await self.bot.say("That is too **low** of a level for you!")
			return
		elif level > player['Level']:
			await self.bot.say("That is too **high** of a level for you!")
			return
		self.LEVEL = level
		self.boss = Boss(self.LEVEL)
		self.boss.summoner = player['Name']
		self.players = {}
		await self.bot.say("A Level {} boss has been summoned".format(self.LEVEL))

	@commands.command(pass_context = True, hidden = True)
	async def respawn(self, ctx):
		'Toggles Auto-Respawning of the Boss'
		self.AUTO_RESPAWN = not self.AUTO_RESPAWN
		await self.bot.say("Auto Respawn is now {}".format(self.AUTO_RESPAWN))

	@commands.command(pass_context = True)
	async def pokeboss(self, ctx):
		'Displays Boss Info'
		if self.boss.isDefeated and self.AUTO_RESPAWN:
			self.boss = Boss(self.LEVEL)
		if not self.boss.hasBeenRevealed:
			await self.bot.say("Boss has not been Revealed!\nPlease use ;pokebattle to fight and reveal the boss.")
			return
		if self.boss.isDefeated:
			await self.bot.say("Level {} Boss **{}** has been defeated!".format(self.LEVEL, self.boss.Name))
			await self.bot.say("Use ;summon to fight a boss of your Level!")
		else:
			await self.bot.say("-= **Boss Pokemon** =-\n*Name*: {0.Name}\n*Health*: {0.Health}/{0.StartingHealth} ({1}%)\n*Level*: {2}\nLast Combo:\n{3}".format(self.boss, round(100*self.boss.Health / self.boss.StartingHealth, 2), self.LEVEL, self.boss.lastUsedCombo))
			await self.bot.send_file(ctx.message.channel, "BossImage.jpg")	
		sorted_Damage = sorted(self.boss.Damage.items(), key=operator.itemgetter(1), reverse=True)
		try:
			await self.bot.say("Most Damage by **{}** with **{}** damage".format(sorted_Damage[0][0].name, sorted_Damage[0][1]))
		except:
			await self.bot.say("Most Damage by *UNKNOWN* with **{}** damage".format(sorted_Damage[0][1]))
		if len(sorted_Damage) >= 2:
			try:
				await self.bot.say("2nd most Damage by *{}* with *{}* damage".format(sorted_Damage[1][0].name, sorted_Damage[1][1]))
			except:
				await self.bot.say("Most Damage by *UNKNOWN* with **{}** damage".format(sorted_Damage[1][1]))
		if len(sorted_Damage) >= 3:
			try:
				await self.bot.say("3rd most Damage by *{}* with *{}* damage".format(sorted_Damage[2][0].name, sorted_Damage[2][1]))
			except:
				await self.bot.say("Most Damage by *UNKNOWN* with **{}** damage".format(sorted_Damage[2][1]))
		if len(sorted_Damage) >= 4:
			await self.bot.say("Assisted by {}".format(", ".join([sorted_Damage[x][0].name for x in range(3, len(sorted_Damage), 1)])))

	@commands.command(pass_context = True)
	async def cd(self, ctx):
		'Shows your Cooldowns'
		msg = ""
		msg += "**Battle**\n"
		if ctx.message.author.id in list(self.players.keys()):
			if self.players[ctx.message.author.id] + COOLDOWN > time.time():
				msg += "You need to wait {} seconds\n".format(round(self.players[ctx.message.author.id] + COOLDOWN - time.time()), 0)
			else:
				msg += "You can battle right now!\n"
		else:
			msg += "You can battle right now!\n"
		msg += "**Train** (*Note: Must be Level 10 to use ;train*)\n"
		if ctx.message.author.id in list(self.training.keys()):
			if self.training[ctx.message.author.id] + TCOOLDOWN > time.time():
				msg += "You need to wait {} seconds".format(round(self.training[ctx.message.author.id] + TCOOLDOWN - time.time()), 0)
			else:
				msg += "You can Train right now!"
		else:
			msg += "You can Train right now!"
		m = await self.bot.say(msg)
		await asyncio.sleep(5	)
		await self.bot.delete_messages([m, ctx.message])

	@commands.command()
	async def pokehelp(self):
		'Pokemon Battle Sim Help'
		await self.bot.say("Welcome to the **Pokemon Battle Simulator**!\nHere you use commands as a group to fight bosses.\nIn order to fight a boss, simply use the *;pokebattle <Moves>* cmd.")
		await self.bot.say("""Crit = 2x Damage and 2% of Max HP\nSuper = 4x Damage and 5% Max HP\nPerfect = 15x Damage and 12% Max HP""")

	@commands.command(pass_context = True)
	async def level(self, ctx):
		'Displays your Current Information'
		with open('Players.json', 'r') as f:
			ALLPLAYERS = json.load(f)
		try:
			player = await self.checkLevel(ALLPLAYERS[ctx.message.author.id])
		except:
			print("NEW PLAYER: {}".format(ctx.message.author.name))
			ALLPLAYERS[ctx.message.author.id] = {"Name" : ctx.message.author.name, "Level": 0, "XP": 0, "Large_Damage" : 0, "Takedowns" : 0}	
			player = ALLPLAYERS[ctx.message.author.id]
		await self.bot.say("**Name**: *{}*\n**Level**: {}\n**XP**: {}/{}\n**Boss Takedowns**: {}\n**Most Dmg in an Attack**: {}".format(player['Name'], player['Level'], player['XP'], await self.ToLevel(int(player['Level']) + 1), player['Takedowns'], player['Large_Damage']))
		with open('Players.json', 'w') as f:
			json.dump(ALLPLAYERS, f)

	@commands.command(pass_context = True)
	async def lookup(self, ctx, member  : discord.Member):
		'Displays your Current Information'
		with open('Players.json', 'r') as f:
			ALLPLAYERS = json.load(f)
		try:
			player = await self.checkLevel(ALLPLAYERS[member.id])
		except:
			await self.bot.say("Could Not find that player!")
			return
		await self.bot.say("**Name**: *{}*\n**Level**: {}\n**XP**: {}/{}\n**Boss Takedowns**: {}\n**Most Dmg in an Attack**: {}".format(player['Name'], player['Level'], player['XP'], await self.ToLevel(int(player['Level']) + 1), player['Takedowns'], player['Large_Damage']))
		with open('Players.json', 'w') as f:
			json.dump(ALLPLAYERS, f)

	@commands.command(pass_context = True, hidden = True)
	async def gamble(self, amount : int):
		if ctx.message.author.id in list(self.gamble.keys()):
			if self.gamble[ctx.message.author.id] + GCOOLDOWN > time.time():
				await self.bot.say("Please wait {} seconds before you can gamble again.".format(round(self.gamble[ctx.message.author.id] + GCOOLDOWN - time.time()), 0))
				return
		with open('Players.json', 'r') as f:
			ALLPLAYERS = json.load(f)
		try:
			player = await self.checkLevel(ALLPLAYERS[ctx.message.author.id])
		except:
			print("NEW PLAYER: {}".format(ctx.message.author.name))
			ALLPLAYERS[ctx.message.author.id] = {"Name" : ctx.message.author.name, "Level": 0, "XP": 0, "Large_Damage" : 0, "Takedowns" : 0}	
			player = ALLPLAYERS[ctx.message.author.id]

		if player['Level'] < 5:
			await self.bot.say("You must be Level 10 to use ;train")
			return
		if player['XP'] < amount:
			await self.bot.say("You don't have that much XP")
			return

		option = random.random() * 100
		if option < 55:
			await self.bot.say("You have lost your offering...")
		elif option < 95:
			await self.bot.say("You have gained back your offering and more!")
		#else:
			# If amount is more than 1/2 level, give back train, else nothing
		with open('Players.json', 'w') as f:
			json.dump(ALLPLAYERS, f)



	@commands.command()
	async def ranking(self):
		with open('Players.json', 'r') as f:
			ALLPLAYERS = json.load(f)
		sorted_players = sorted(ALLPLAYERS.items(), key=self.getLevel, reverse=True)
		ret = ""
		#print(sorted_players)
		# for p in sorted_players[:4]:
		# 	player = p[1]
		# 	try:
		# 		#ret += "**{}**, Level: *{}*, Most Damage Done in a Single Attack: *{}*, Boss Takedowns: {}".format(player['Name'], player["Level"], player['Large_Damage'], player['Takedowns'])
		# 	except:
		# 		ALLPLAYERS[p[0]]['Large_Damage'] = 0
		# 		ALLPLAYERS[p[0]]["Takedowns"] = 0
		# 		#ret += "**{}**, Level: *{}*, Most Damage Done in a Single Attack: *{}*, Boss Takedowns: {}".format(player['Name'], player["Level"], player['Large_Damage'], player['Takedowns'])
		# 	ret += "\n"

		# 1st
		first = sorted_players[0][1]
		ret += ":first_place: **{}** Level **{}**\n".format(first['Name'], first['Level'])

		second = sorted_players[1][1]
		ret += ":second_place: {} Level {}\n".format(second['Name'], second['Level'])

		third = sorted_players[2][1]
		ret += ":third_place: {} Level {}\n".format(third['Name'], third['Level'])

		fourth = sorted_players[3][1]
		ret += ":medal: {} Level {}\n".format(fourth['Name'], fourth['Level'])

		fifth = sorted_players[4][1]
		ret += ":medal: {} Level {}".format(fifth['Name'], fifth['Level'])		


		await self.bot.say(ret)
		with open('Players.json', 'w') as f:
			json.dump(ALLPLAYERS, f)

	def getLevel(self, dict):
		return dict[1]['Level']

	async def giveXP(self, member , XP : int):
		with open('Players.json', 'r') as f:
			ALLPLAYERS = json.load(f)
		try:
			player = ALLPLAYERS[member.id]
		except:
			print("NEW PLAYER: {}".format(ctx.message.author.name))
			ALLPLAYERS[ctx.message.author.id] = {"Name" : ctx.message.author.name, "Level": 0, "XP": 0, "Large_Damage" : 0, "Takedowns" : 0}	
				
		ALLPLAYERS[member.id]["XP"] = ALLPLAYERS[member.id]["XP"] + XP

		with open('Players.json', 'w') as f:
				json.dump(ALLPLAYERS, f)

	@commands.command(pass_context = True)
	async def train(self, ctx):
		"Fights Pokemon for XP"
		if ctx.message.author.id in list(self.training.keys()):
			if self.training[ctx.message.author.id] + TCOOLDOWN > time.time():
				await self.bot.say("Please wait {} seconds before you can train again.".format(round(self.training[ctx.message.author.id] + TCOOLDOWN - time.time()), 0))
				return
		with open('Players.json', 'r') as f:
			ALLPLAYERS = json.load(f)
		try:
			player = await self.checkLevel(ALLPLAYERS[ctx.message.author.id])
		except:
			print("NEW PLAYER: {}".format(ctx.message.author.name))
			ALLPLAYERS[ctx.message.author.id] = {"Name" : ctx.message.author.name, "Level": 0, "XP": 0, "Large_Damage" : 0, "Takedowns" : 0}	
			player = ALLPLAYERS[ctx.message.author.id]

		if player['Level'] < 10:
			await self.bot.say("You must be Level 10 to use ;train")
			return

		# Fight (LEVEL/4 + 1 to LEVEL Pokemon)
		# Levels from 1 to 2 * LEVEL
		# Percent to win = LEVEL / 2 / level * 100

		Enemies = [Enemy(getRandomName(), random.randrange(1, 2*player['Level'])) for x in range(int(player['Level']/4), int(player['Level']/2) + 1, 1)]

		toPrint = ""
		XP = 0
		for enemy in Enemies:
			percent_to_kill = player['Level'] / 2 / enemy.level * 100
			if percent_to_kill > 90:
				percent_to_kill = 90
			if random.random() * 100 < percent_to_kill:
				kill_xp = int(player['Level'] * (100 - percent_to_kill) / 2)
				XP += kill_xp
				toPrint += "You **Beat** a Level {} **{}** for {} XP ({}% to beat)\n".format(enemy.level, enemy.name, kill_xp, int(percent_to_kill))
			else:
				toPrint += "You **Lost** to a Level {} **{}** ({}% to beat)\n".format(enemy.level, enemy.name, int(percent_to_kill))

		if random.random() <= 0.40:
			toPrint += "You use a **Lucky Egg** to gain more XP!\n"
			XP = XP * 1.5

		pokelootText = ""
		if random.random() <= 0.25:
			pokeloot = await self.ToLevel(player['Level'] + 1) * 0.20 + 1
			pokelootText = "You Find a **Pokeloot** worth {} XP\n".format(int(pokeloot))
			if random.random() <= 0.20:
				pokeloot += await self.ToLevel(player['Level'] + 1) * 0.45 + 1
				pokelootText = "You Find a **Great Pokeloot** worth {} XP\n".format(int(pokeloot))
				if random.random() <= 0.20:
					pokeloot += await self.ToLevel(player["level"] + 1) + 1
					pokelootText = "You Find an **Ultra Pokeloot** worth {} XP\n".format(int(pokeloot))
					if random.random() <= 0.10:
						pokeloot += await self.ToLevel(player["level"] + 1) * 2 + 1
						pokelootText = "You Find an **Masterball Pokeloot** worth {} XP\n".format(int(pokeloot))
			toPrint += pokelootText
			XP += pokeloot

		XP = int(XP)
		await self.bot.say(toPrint)
		await self.giveXP(ctx.message.author, XP)
		await self.bot.say("You trained for {} XP!".format(XP))
		self.training[ctx.message.author.id] = time.time()

	@commands.command()
	async def types(self):
		val = """ -= **Possible Types ** =-
:regional_indicator_n: ormal\n:regional_indicator_f: ire
:regional_indicator_w: ater\n:regional_indicator_g: rass
:regional_indicator_p: oison\n:regional_indicator_d: ragon
:regional_indicator_s: teel\n:regional_indicator_e: lectric
:regional_indicator_b: ug\n:regional_indicator_i: ce"""
		await self.bot.say(val)

	async def ToLevel(self, level):
		if level >= 100:
			return 0
		return int(math.pow(level, 3))

	async def checkLevel(self, player):
		while player['XP'] >= await self.ToLevel(int(player['Level']) + 1) and player['Level'] is not 100:
			player['XP'] -= await self.ToLevel(int(player['Level']) + 1)
			player['Level'] += 1
		return player

class Boss:
	def __init__(self, level):
		global NUM_MOVES
		if level <= 10:
			NUM_MOVES = 5
		elif level <= 25:
			NUM_MOVES = 8
		elif level <= 40:
			NUM_MOVES = 10
		elif level <= 65:
			NUM_MOVES = 12
		elif level <= 80:
			NUM_MOVES = 15
		else:
			NUM_MOVES = 18
		self.Health = random.randrange(30*NUM_MOVES, 125*NUM_MOVES) * level
		self.StartingHealth = self.Health
		self.Name = getRandomName()
		self.Image = getImage(self.Name)
		self.Name = self.Name.capitalize()
		self.Damage = {}
		self.isDefeated = False
		self.hasBeenRevealed = False
		self.combination = [random.choice(["N","F","W","G","P","D","S","E","B","I"]) for x in range(0, NUM_MOVES, 1)]
		self.lastUsedCombo = ""
		self.summoner = ""

	def change1(self):
		choose = random.choice(range(0, NUM_MOVES, 1))
		self.combination[choose] = random.choice(["N","F","W","G","P","D","S","E","B","I"])

class Enemy:
	def __init__(self, name, level):
		self.name = name.capitalize()
		self.level = level

def setup(bot):
	bot.add_cog(Games(bot))