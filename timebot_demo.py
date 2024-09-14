import discord
from discord.ext import commands
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
import requests

# Define the intents for your bot
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

# Set up the bot with a command prefix and the defined intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def time(ctx, *, city: str):
    try:
        # Fetch city coordinates using OpenCage API
        geocode_url = f'https://api.opencagedata.com/geocode/v1/json?q={city}&key=YOUR_OPENCAGE_API_KEY'
        response = requests.get(geocode_url)
        data = response.json()

        # Check if the API returned any results
        if data['results']:
            # Extract latitude and longitude
            coordinates = data['results'][0]['geometry']
            lat, lng = coordinates['lat'], coordinates['lng']

            # Find the timezone for the coordinates
            tf = TimezoneFinder()
            timezone_str = tf.timezone_at(lng=lng, lat=lat)

            # Handle cases where no timezone is found
            if timezone_str:
                timezone = pytz.timezone(timezone_str)
                city_time = datetime.now(timezone)
                await ctx.send(f'The current time in {city.title()} is {city_time.strftime("%Y-%m-%d %H:%M:%S")}')
            else:
                await ctx.send(f'Timezone not found for {city.title()}.')
        else:
            await ctx.send('City not found. Please try another city or check your spelling.')
    except Exception as e:
        await ctx.send('An error occurred: ' + str(e))

# Run the bot with your token
bot.run('YOUR_DISCORD_BOT_TOKEN')
