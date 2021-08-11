# bot.py
import os
import random

from discord.ext import commands
from dotenv import load_dotenv
import requests
import wikipedia

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='chuck', help='Responds with a random joke from Chuck Norris')
async def chuck(ctx):
    response = requests.get("https://api.chucknorris.io/jokes/random").json()
    await ctx.send(response['value'])

@bot.command(name='roll', help='Roll the dice.')
async def roll(ctx):
    response = random.randrange(1, 7)
    await ctx.send(f"You rolled a {response}! 🎲")

# BUGFIX NEEDED
@bot.command(name='wiki', help='Search for information on Wikipedia.')
async def roll(ctx):

    response = []

    def wiki_search(title):
        return [title, wikipedia.summary(title)]

    try:
        title = wikipedia.search(word)[0]
        wiki_search(title)
    except:
        suggest = wikipedia.suggest(word)
        if suggest is None:
            print("Not found.")
        else:
            wiki_search(suggest.capitalize())

    await ctx.send(f"You rolled a {response}! 🎲")

bot.run(TOKEN)