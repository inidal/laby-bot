# bot.py
import os
import random

import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv
import requests
import wikipedia
from bs4 import BeautifulSoup
import datetime

load_dotenv()

# Tokens/Keys
TOKEN = os.getenv('DISCORD_TOKEN')
OPENWEATHER = os.getenv('OPENWEATHER_KEY')
IMDB_KEY = os.getenv('IMDB_KEY')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    anniversary.start()
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def ping(ctx):
    ''' Checking if laby is working '''

    embed = discord.Embed(title='Pong 🏓',
                          description="I'm perfectly working.",
                          color = discord.Colour.green())

    await ctx.send(embed=embed)

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

    embed.set_thumbnail(
        url=f"http://openweathermap.org/img/w/{response['weather'][0]['icon']}.png"
    )

    # Temperature (min, average, max)
    embed.add_field(name="🌡 Min.", value=f'{"{:.2f}".format(float(response["main"]["temp_min"]) - 273.15)}°C', inline=True)
    embed.add_field(name="🌡 Avg.", value=f'{"{:.2f}".format(float(response["main"]["temp"]) - 273.15)}°C', inline=True)
    embed.add_field(name="🌡 Max.", value=f'{"{:.2f}".format(float(response["main"]["temp_max"]) - 273.15)}°C', inline=True)

    # Humidity, cloudiness, wind speed
    embed.add_field(name="💧 Humidity", value=f'{response["main"]["humidity"]}%', inline=True)
    embed.add_field(name="☁ Clouds", value=f'{response["clouds"]["all"]}% cloudiness', inline=True)
    embed.add_field(name="💨 Wind", value=f'{response["wind"]["speed"]} m/sec', inline=True)

    await ctx.send(embed=embed)

@bot.command(name='imdb', help='IMDb.')
async def imdb(ctx, *args):

    user_input = ' '.join(word for word in args)

    # Endpoint
    url = "https://imdb8.p.rapidapi.com/auto-complete"
    querystring = {"q": user_input}

    # Header parameters
    headers = {
        'x-rapidapi-key': IMDB_KEY,
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

    # Get show ID
    try:
        response = requests.request("GET", url, headers=headers, params=querystring).json()
        show_id = response['d'][0]
    except KeyError:
        embed = discord.Embed(description=f"{user_input} not found! Sorry.", color=discord.Colour.blue())
        await ctx.send(embed=embed)
        return

    # Get overview details
    url2 = "https://imdb8.p.rapidapi.com/title/get-overview-details"
    querystring2 = {"tconst": f"{show_id['id']}", "currentCountry": "US"}

    response2 = requests.request("GET", url2, headers=headers, params=querystring2).json()

    # Summary
    try:
        summary = response2['plotSummary']['text']
    except KeyError:
        summary = response2['plotOutline']['text']

    embed = discord.Embed(
        title=f"{response2['title']['title']} ({show_id['q'] if show_id['q'] == 'TV series' or show_id['q'] == 'TV mini-series' else show_id['y']})",
        description= summary,
        color = discord.Colour.blue()
    )

    # Thumbnail
    embed.set_thumbnail(url=response2['title']['image']['url'])
    embed.set_image(url=response2['title']['image']['url'])

    genres = ', '.join(genre for genre in response2['genres'])

    embed.add_field(name="Genres", value=f"{genres}", inline=True)
    embed.add_field(name="Running time", value=response2['title']['runningTimeInMinutes'], inline=True)
    embed.add_field(name="Rating", value=response2['ratings']['rating'], inline=True)


    if response['d'][0]['q'] == 'TV series' or response['d'][0]['q'] == 'TV mini-series':

        # Start year
        embed.add_field(name="Started", value=response2['title']['seriesStartYear'], inline=True)

        # If series has ended, otherwise in progress
        try:
            embed.add_field(name="Finished", value=response2['title']['seriesEndYear'], inline=True)
        except KeyError:
            embed.add_field(name="Finished", value="In progress", inline=True)

        # Number of episodes
        embed.add_field(name="Episodes", value=response2['title']['numberOfEpisodes'], inline=True)



    # Trailer video
    embed.add_field(name="Trailer", value=f"https://www.imdb.com/video/{response['d'][0]['v'][0]['id']}", inline=False)


    await ctx.send(embed=embed)

# Uncomment Giphy API and embed.set_image
@tasks.loop(hours=24)
async def anniversary():

    # Get specific channel
    channel = bot.get_channel(690019953763811448)

    # Giphy API
    # url = "https://api.giphy.com/v1/gifs/random?api_key=zTAsnQJhdwptUkRKmC1hKBbFeb7FXXC0&tag=happy+birthday&rating=g"
    # giphy_response = requests.request("GET", url).json()

    # Anniversaries list
    anniversaries = [
        ['Edmyr', '01-28', '5537'], # Nidal
        ['Qiujin', '04-01', '1737'], # Amine
        ['Acrid', '04-03', '0332'], # Hajar
        ['Marijanna', '08-01', '7262'], # Anas
        ['thexfighter', '08-18', '9307'], # Mehdi
        ['mounami', '12-28', '3190'], # Anouar
        ['Jane', '08-15', '3190'],  # TEST
        ['Edmyr', '08-16', '5537']  # TEST
    ]

    def check_anniversary():

        names = []

        for i, j, k in anniversaries:
            check = str(datetime.date.today())[5:] == j
            names.append(i) if check else None

        happyb_list = ", ".join(name for name in names)

        return happyb_list if len(happyb_list) > 1 else None

    # Embed message
    embed = discord.Embed(
        title='Happy birthday time',
        description= f'🎂 @everyone !! Say Happy Birthday to {check_anniversary()} ! 🎉🎉🎈🎈',
        color = discord.Colour.magenta()
    )

    # embed.set_image(url=giphy_response['data']['image_original_url'])

    # If anniversary then PARTY
    if check_anniversary() is not None:
        await channel.send(embed=embed)

@bot.command(name='docs', help='Looking for docs on Google')
async def docs(ctx, *args):

    user_input = '+'.join(word for word in args)

    google_link = f'https://www.google.com/search?client=opera&q=-inurl%3Ahtm+-inurl%3Ahtml+intitle%3A"index+of"+%2B("%2Febooks"%7C"%2Fbook")+%2B(mobi%7Cpdf%7Cepub)+%2B"{user_input}"'
    embed = discord.Embed(
        title='🔍 Open your Google Search result.',
        url= google_link,
        color=discord.Colour.blue()
    )

    await ctx.send(embed=embed)

bot.run(TOKEN)