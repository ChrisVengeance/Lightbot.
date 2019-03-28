@client.commant(pass_context = True)
@commands.has_permissions(ban_members=True)
async def ban(member: discord.Member, days: int = 7):
if "226028320104382464" in [role.id for role in message.in.author.roles]:
    await client.ban(member, days)
  else:
  await client.say("You don't have permission to use this command.")
  
  
  
  
  @client.command(pass_context = True)
  @commands.has_permissions(kick_members=True)
    async def kick(ctx, userName: discord.User):
      pass
      """Kicks a user From Server"""
      await.client.kick(userName)
      await client.say("__**Successfully Kicked User From Server!**__")
			
			#Public Welcome
@bot.event
async def on_member_join(member):
    print("Reconized that " + member.name + " joined")
    await bot.send_message(member, newUserDMMessage)
    await bot.send_message(discord.object(id='welcome'), 'Welcome to Lynx Gaming')
    print("Sent message to " + member.name)
    print("Sent message about " + member.name + " to welcome")
			
			
      
  
	
	#Mod Leave Announcement
@bot.event
async def on_member_remove(member):
    print("Reconized that " + member.name + "left")
    await bot.send_message(discord.Object(id= '#left'), '**' + member.mention + '** Has Left The Server.')
    print("Sent message to #left")
		
		
		
		
		
		
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
		
	
  
  
  
