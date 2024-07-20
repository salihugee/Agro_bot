from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

# Define the bot token
BOT_TOKEN = 7235160397:AAHPQzKelRMIAy2B_zZZZRdxuFMJAWZ71eQ

# Define the start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Hello! I am your Agriculture Bot. I can help you with weather updates, crop management tips, market prices, and more!')

# Define a simple function to fetch weather updates
def get_weather(location):
    api_key = 'YOUR_WEATHER_API_KEY'
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
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

# Main function to start the bot
def main() -> None:
    updater = Updater(BOT_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("weather", weather))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
