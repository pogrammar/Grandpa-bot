import random 
import asyncio

words = ["No one gets to see the words hehe"]  

images =   ['```\n   +---+\n   O   | \n  /|\\  | \n  / \\  | \n      ===```',   
			'```\n   +---+ \n   O   | \n  /|\\  | \n  /    | \n      ===```', 
			'```\n   +---+ \n   O   | \n  /|\\  | \n       | \n      ===```', 
			'```\n   +---+ \n   O   | \n  /|   | \n       | \n      ===```', 
			'```\n   +---+ \n   O   | \n   |   | \n       | \n      ===```', 
			'```\n   +---+ \n   O   | \n       | \n       | \n      ===```', 
			'```\n  +---+ \n      | \n      | \n      | \n     ===```']
async def play(bot, ctx):
	def check(m):
		return m.author == ctx.author
	guesses = '' 
	turns = 6
	word = random.choice(words) 
	msg = await ctx.respond("**Guess the characters**:\nType`Exit` to leave the game\n")
	guess_msg = await ctx.send(images[turns])
	word_msg = await ctx.send(f"`{' '.join('_'*len(word))}`")
	while turns > 0: 
		out = ''
		rem_chars = 0
		for char in word:  
			if char in guesses:  
				out += char
			else:  
				out += '_'
				rem_chars += 1
		await word_msg.edit(content=f"`{' '.join(out)}`")
		
		if rem_chars == 0: 
			await word_msg.edit(content=f'**{word}**')
			return await ctx.send("**You Win :trophy:**")

		msg = await bot.wait_for('message', check=check, timeout=20.0)
		if msg.content == 'exit':
			await ctx.send("You quit")
			return
		if msg.content == word:
			await word_msg.edit(content=f'**{word}**')
			await ctx.send("**You Win :trophy:**")
			return

		guess =  msg.content[0]
		guesses += guess  
		await msg.delete()

		if guess not in word: 
			turns -= 1
			await ctx.send("Wrong :x:", delete_after=1.0) 
			await guess_msg.edit(content=images[turns])
			if turns == 0:
				await word_msg.edit(content=f'**{word}**')
				return await ctx.send("You Loose :x:")
