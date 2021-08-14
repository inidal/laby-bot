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
OPENWEATHER = os.getenv('OPENWEATHER_KEY')

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

    embed = discord.Embed(description = f"You rolled a {response}! 🎲",
                          color = discord.Colour.blue())

    await ctx.send(embed=embed)

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

    URL = "https://dog.ceo/api/breeds/image/random"
    page = requests.get(URL)
    image = page.json()['message']

    embed = discord.Embed(title="Here's your adorable dog",
                          color=discord.Colour.blue())

    embed.set_image(url=image)

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

@bot.command(name='weather', help='Weather.')
async def weather(ctx, *args):

    city = ' '.join(word for word in args)
    URL = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER}'
    response = requests.get(URL).json()

    embed = discord.Embed(
        title=f'{response["weather"][0]["description"].capitalize()} in {response["name"]}, {response["sys"]["country"]}',
        color = discord.Colour.blue()
    )

    # embed.set_image(url=challenge["image"])
    embed.set_thumbnail(
        url=f"http://openweathermap.org/img/w/{response['weather'][0]['icon']}.png"
    )

    embed.add_field(name="🌡 Avg. Temperature", value=f'{"{:.2f}".format(float(response["main"]["temp"]) - 273.15)}°C', inline=True)
    embed.add_field(name="🌡 Min", value=f'{"{:.2f}".format(float(response["main"]["temp_min"]) - 273.15)}°C', inline=True)
    embed.add_field(name="🌡 Max", value=f'{"{:.2f}".format(float(response["main"]["temp_max"]) - 273.15)}°C', inline=True)


    embed.add_field(name="💧 Humidity", value=f'{response["main"]["humidity"]}%', inline=True)
    embed.add_field(name="☁ Clouds", value=f'{response["clouds"]["all"]}% cloudiness', inline=True)
    embed.add_field(name="💨 Wind", value=f'{response["wind"]["speed"]} meters per second', inline=True)




    await ctx.send(embed=embed)


# @bot.command(name='test', help='Testing command.')
# async def test(ctx, *args):
#
#     await ctx.send(f"{result}")


bot.run(TOKEN)