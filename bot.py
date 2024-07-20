from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, CallbackContext
import requests
import os

app = Flask(__name__)

# Initialize bot and dispatcher
BOT_TOKEN = '7235160397:AAHPQzKelRMIAy2B_zZZZRdxuFMJAWZ71eQ'
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  # Set this environment variable in Render

bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

# Define the start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Hello! I am your Agriculture Bot. I can help you with weather updates, crop management tips, market prices, and more!')

# Define a simple function to fetch weather updates
def get_weather(location):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}"
    response = requests.get(base_url).json()
    if response['cod'] != '404':
        main = response['main']
        weather_description = response['weather'][0]['description']
        return f"Temperature: {main['temp']}K\nWeather: {weather_description}"
    else:
        return "Location not found"

# Define the weather command handler
def weather(update: Update, context: CallbackContext) -> None:
    location = ' '.join(context.args)
    weather_info = get_weather(location)
    update.message.reply_text(weather_info)

# Add command handlers to dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("weather", weather))

# Route to handle webhook updates
@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

# Root route for health check
@app.route('/')
def index():
    return 'Bot is running!'

if __name__ == '__main__':
    app.run(port=8443)
