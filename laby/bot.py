# bot.py
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
import wikipedia
from bs4 import BeautifulSoup

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='chuck', help='Responds with a random joke from Chuck Norris')
async def chuck(ctx):
    response = requests.get("https://api.chucknorris.io/jokes/random").json()
    embed = discord.Embed(description = response['value'],
                          color = discord.Colour.blue())

    embed.set_thumbnail(url = response['icon_url'])

    await ctx.send(embed=embed)

@bot.command(name='roll', help='Roll the dice.')
async def roll(ctx):
    response = random.randrange(1, 7)
    await ctx.send(f"You rolled a {response}! 🎲")

@bot.command(name='wiki', help='Search for information on Wikipedia.')
async def roll(ctx, *args):

    word = ' '.join(word for word in args)
    result = []

    def wiki_search(title):
        result.append(title)
        if len(wikipedia.summary(title)) > 1500:
            result.append(wikipedia.summary(title, sentences=3))
        else:
            result.append(wikipedia.summary(title))
        result.append(wikipedia.page(title).url)

    try:
        title = wikipedia.search(word)[0]
        wiki_search(title)
    except:
        suggest = wikipedia.suggest(word)
        if suggest is None:
            await ctx.send("There were no results matching the query.")
        else:
            wiki_search(suggest.capitalize())

    embed = discord.Embed(
        title = result[0],
        url = result[2],
        description = result[1],
        color = discord.Colour.blue()
    )

    await ctx.send(embed=embed)

@bot.command(name='dog', help='Random dog image.')
async def dog(ctx):

    URL = "https://random.dog/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    try:
        image = soup.find(id="dog-img")['src']
    except:
        image = soup.find(id="dog-img").source['src']

    embed = discord.Embed(title="Here's your adorable dog",
                          color=discord.Colour.blue())

    embed.set_image(url=f'{URL}{image}')

    await ctx.send(embed=embed)

@bot.command(name='cat', help='Random cat image.')
async def cat(ctx):

    URL = "http://random.cat"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    image = soup.find(id="cat")['src']

    embed = discord.Embed(title="Here's your adorable cat",
                          color=discord.Colour.blue())

    embed.set_image(url=image)

    await ctx.send(embed=embed)


@bot.command(name='test', help='Testing command.')
async def test(ctx, *args):
    arguments = args
    result = ' '.join(word for word in arguments)

    await ctx.send(f"{result}")


bot.run(TOKEN)