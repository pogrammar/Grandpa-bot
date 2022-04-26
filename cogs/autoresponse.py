import discord
from discord.ext import commands
import asyncio
import random
   

class AutoResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        msg1 = "I'm Dad!"
        msg1_responses = ["Hi dad, i'm Grandpa! ",
                            "Son- they probably know by now.",
                            "Dad, im your dad.",
                            "Son, I cant figure out how to get my discord to open, can I have help?",
                            "You should be working right now, your job is at a high risk.",
                            "bruh",
                            "They havent forgotten you...",
                            "They remember you son.",
                            "Ive been catching up on my memes, and I just learnt the meme- oh wait I forgor",
                            "Son, what is Amogus?",
                            "ok ok ok but how do I get my phone to open",
                            "Listen here i need suggestions give me some"
                            ]
        if msg1 in message.content:
            msg_response = random.choice(msg1_responses)
            await message.channel.send(msg_response)
            return


        msg2 = "Keep your voice down!"
        msg2_responses = ["Son please tell them to stop, my ears start hurting",
                            "Son They were talking to me, my hearing aid's malfunctional ??",
                            "Son can you think before speaking? They were talking to me. If you keep forgetting to buy me a new hearing aid, then this **will** happen.",
                            "They are right, please dont speak that loud, my ears start hurting.",
                            "You can let them speak loud, it gets kind of boring in here.",
                            "Keep YOUR voice down bru-"
                            ]
        
        if msg2 in message.content:
            msg_response = random.choice(msg2_responses)
            await message.channel.send(msg_response)
            return

        msg3 = "d!embarrass"
        msg3_responses = ["My lessons paid off ??",
                            "Son this is NOT the correct usage of my lessons. I am very dissapointed.",
                            "I wouldnt do that even IF I was reqested to ??",
                            "damn- ??",
                            "Stop it! they feep bad!",
                            "No. Son detention for a literal **second** ",
                            "Son was this your doing?",
                            "He just wont listen! why does he keep doing this!"
                            ]
        
        if msg3 in message.content:
            msg_response = random.choice(msg3_responses)
            await asyncio.sleep(1)
            await message.channel.send(msg_response)
            return

        
def setup(bot):
    bot.add_cog(AutoResponse(bot))