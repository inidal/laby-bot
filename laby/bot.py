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
import json
from googletrans import Translator

load_dotenv()

# Tokens/Keys
TOKEN = os.getenv('DISCORD_TOKEN')
OPENWEATHER = os.getenv('OPENWEATHER_KEY')
IMDB_KEY = os.getenv('IMDB_KEY')
GIPHY_KEY = os.getenv('GIPHY_KEY')
TENOR_KEY = os.getenv('TENOR_KEY')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    anniversary.start()
    await bot.change_presence(activity=discord.Game(name="with the Universe"))
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def ping(ctx):
    ''' Checking if laby is working '''

    embed = discord.Embed(title='Pong 🏓',
                          description="I'm perfectly working.",
                          color = discord.Colour.green())

    await ctx.send(embed=embed)

@bot.command(name='man', help='Get help with this command', hidden=True)
@commands.is_owner()
async def man(ctx):
    ''' Get help with these commands '''

    embed = discord.Embed(title='📃 Commands',
                          description="As simple as that.",
                          color = discord.Colour.green())

    embed.add_field(name="`!ping`", value='Checking if @laby is alive', inline=True)
    embed.add_field(name="`!chuck`", value='A random Chuck fact', inline=True)
    embed.add_field(name="`!roll`", value='If you like to roll the dice', inline=True)
    embed.add_field(name="`!wiki <value>`", value='Get a summary from Wiki', inline=True)
    embed.add_field(name="`!dog`", value='The best therapist has fur and four legs', inline=True)
    embed.add_field(name="`!cat`", value="If cats could talk, they wouldn't", inline=True)
    embed.add_field(name="`!weather <value>`", value='Get the weather from OpenWeather', inline=True)
    embed.add_field(name="`!imdb <value>`", value='Get info about a movie/tvshow from IMDb', inline=True)
    embed.add_field(name="`!docs <value>`", value='Looking for a document?', inline=True)
    embed.add_field(name="`!gif <value>`", value='Search for a GIF', inline=True)
    embed.add_field(name="`!translate <lang_code> <text>`", value='Use Google Translate to translate a word/sentence.', inline=True)

    await ctx.send(embed=embed)

@bot.command(name='chuck', help='A random Chuck fact.')
async def chuck(ctx):
    response = requests.get("https://api.chucknorris.io/jokes/random").json()

    embed = discord.Embed(title = 'Random Chuck Norris Joke (Fact)',
                          description = response['value'],
                          color = discord.Colour.blue())

    embed.set_thumbnail(url = response['icon_url'])

    await ctx.send(embed=embed)

@bot.command(name='roll', help='If you like to roll the dice.')
async def roll(ctx):
    response = random.randrange(1, 7)

    embed = discord.Embed(description = f"You rolled a {response}! 🎲",
                          color = discord.Colour.blue())

    await ctx.send(embed=embed)

@bot.command(name='wiki', help='Get a summary from Wiki.')
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

@bot.command(name='dog', help='The best therapist has fur and four legs.')
async def dog(ctx):

    URL = "https://dog.ceo/api/breeds/image/random"
    page = requests.get(URL)
    image = page.json()['message']

    embed = discord.Embed(title="Here's your adorable dog",
                          color=discord.Colour.blue())

    embed.set_image(url=image)

    await ctx.send(embed=embed)

@bot.command(name='cat', help="If cats could talk, they wouldn't.")
async def cat(ctx):

    URL = "http://random.cat"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    image = soup.find(id="cat")['src']

    embed = discord.Embed(title="Here's your adorable cat",
                          color=discord.Colour.blue())

    embed.set_image(url=image)

    await ctx.send(embed=embed)

@bot.command(name='weather', help='Get the weather from OpenWeather.')
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

@bot.command(name='imdb', help='Get info about a movie/tvshow from IMDb.')
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
    channel = bot.get_channel(417397521451843599)

    # Giphy API
    url = f"https://api.giphy.com/v1/gifs/random?api_key={GIPHY_KEY}&tag=happy+birthday&rating=g"
    giphy_response = requests.request("GET", url).json()

    # Quote API
    quote = requests.get("https://type.fit/api/quotes").json()

    # Anniversaries list
    anniversaries = [
        ['Edmyr', '01-28', '5537'],
        ['Qiujin', '04-01', '1737'],
        ['Acrid', '04-03', '0332'],
        ['Marijanna', '08-01', '7262'],
        ['thexfighter', '08-18', '9307'],
        ['mounami', '12-28', '3190']
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
        title="IT'S YOUR DAY — Happy Birthday!",
        description= f"🎂 @everyone !! Say Happy Birthday to {check_anniversary()} ! 🎉🎉🎈🎈",
        color = discord.Colour.magenta()
    )
    random_quote = random.randint(0, len(quote))
    embed.set_image(url=giphy_response['data']['image_original_url'])
    embed.set_footer(text=f'{quote[random_quote]["text"]} — {quote[random_quote]["author"]}')

    # If anniversary then PARTY
    if check_anniversary() is not None:
        await channel.send(embed=embed)

@bot.command(name='docs', help='Looking for a document?', hidden=True)
@commands.is_owner()
async def docs(ctx, *args):

    user_input = '+'.join(word for word in args)

    google_link = f'https://www.google.com/search?client=opera&q=-inurl%3Ahtm+-inurl%3Ahtml+intitle%3A"index+of"+%2B("%2Febooks"%7C"%2Fbook")+%2B(mobi%7Cpdf%7Cepub)+%2B"{user_input}"'
    embed = discord.Embed(
        title='🔍 Open your Google Search result.',
        url= google_link,
        color=discord.Colour.blue()
    )

    await ctx.send(embed=embed)

@bot.command(name='gif', help='Search for a GIF.')
async def gif(ctx, *args):

    # our test search
    search_term = '+'.join(word for word in args)
    desc_keywords = ' '.join(word for word in args)
    lmt = 50

    # get the top 8 GIFs for the search term
    r = requests.get(
        "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, TENOR_KEY, lmt))

    embed = discord.Embed(
        title='The gif your asked for',
        description= f'Your `{desc_keywords}` GIF.',
        color = discord.Colour.blue()
    )

    if r.status_code == 200:
        # load the GIFs using the urls for the smaller GIF sizes
        top_50gifs = json.loads(r.content)
        embed.set_image(url=top_50gifs["results"][random.randint(0, 49)]['media'][0]['gif']['url'])
        await ctx.send(embed=embed)
    else:
        top_50gifs = None
        await ctx.send("Nothing found.")

@bot.command(name='translate', help='Use Google Translate to translate a word/sentence.')
async def docs(ctx, arg, *args):
    translator = Translator()

    text_to_trans = ' '.join(word for word in args)

    # Translation in action
    try:
        trans_operation = translator.translate(text_to_trans, dest=arg).text
    except ValueError:
        embed = discord.Embed(
            title= "Usage: !translate <lang_code> <text>",
            description= '[You can get the language names by code here](https://meta.wikimedia.org/wiki/Template:List_of_language_names_ordered_by_code)',
            color=discord.Colour.red()
        )

        await ctx.send(embed=embed)
        return

    embed = discord.Embed(
        description=trans_operation,
        color=discord.Colour.blue()
    )

    await ctx.send(embed=embed)


bot.run(TOKEN)
