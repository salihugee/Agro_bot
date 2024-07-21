from flask import Flask, request
import requests
import threading
import time

# Telegram Bot API token
TOKEN = '7235160397:AAHPQzKelRMIAy2B_zZZZRdxuFMJAWZ71eQ'
# Your app URL
KEEP_ALIVE_URL = 'https://agro-bot.onrender.com/'
# OpenWeatherMap API key
WEATHER_API_KEY = 'your_openweathermap_api_key'

app = Flask(__name__)

@app.route(f'/{TOKEN}', methods=['POST'])
def respond():
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        if text == "/start":
            response = "Hello! I am your Agriculture Bot."
        elif text.startswith("/weather"):
            location = text.split("/weather", 1)[1].strip()
            response = get_weather(location)
        else:
            response = "I don't understand that command."

        send_message(chat_id, response)
    return "ok", 200

def get_weather(location):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            return f"Error: {data['message']}"

        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        return f"The weather in {location} is {weather} with a temperature of {temperature}°C."
    except Exception as e:
        return f"An error occurred: {e}"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

def keep_alive():
    while True:
        try:
            requests.get(KEEP_ALIVE_URL)
        except Exception as e:
            print(f"Keep-alive ping failed: {e}")
        time.sleep(25 * 60)  # Ping every 25 minutes

if __name__ == "__main__":
    # Start the keep-alive pinging in a separate thread
    threading.Thread(target=keep_alive).start()
    app.run(host='0.0.0.0', port=5000)
