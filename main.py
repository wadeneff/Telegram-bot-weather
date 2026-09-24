import telebot
import requests
import json
from config import api_key
from telebot import types

bot = telebot.TeleBot(api_key)
api = 'effd69c38e8373f0fb540676eff86681'

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Рад вас видеть, {message.from_user.first_name}, напишите свой город.')

@bot.message_handler(content_types=['text'])
def getWeather(message):
    cityForApi = message.text.strip().lower()
    city = message.text.strip()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={cityForApi}&appid={api}&units=metric')
    data = json.loads(res.text)

    if str(data['cod']) == '404':
        bot.send_message(message.chat.id, 'Город не найден, попробуйте ещё раз.')
        return
    else:
        temp = data['main']['temp']
        tempFeelsLike = data['main']['feels_like']
        clouds = data['weather'][0]['description']

        weather_emoji = {
            'clear sky': '☀️ Ясно',
            'few clouds': '⛅️ Переменная облачность',
            'scattered clouds': '⛅️ Небольшая облачность',
            'broken clouds': '🌥 Облачно',
            'overcast clouds': '☁️ Сплошная облачность',
            'light rain': '🌦 Небольшой дождь',
            'moderate rain': '🌧 Дождь',
            'mist': '🌫 Туман',
        }
        cloudsForUser = weather_emoji.get(clouds, f'🌡 {clouds.capitalize()}')

        bot.send_message(message.chat.id, f'Температура в городе {city} сейчас {round(temp)}℃\nОщущается как {round(tempFeelsLike)}℃\n{cloudsForUser}')


bot.polling(non_stop=True)