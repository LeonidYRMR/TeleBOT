import telebot
from telebot import types
import pyowm
from pyowm import OWM
from pyowm.utils.config import get_default_config

token = '1902741146:AAHIF5gGl-YlyG8GNGZlDjJHLlkUvqXrwmE'

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет ✌️\nЯ бот погоды, нажми кнопку, чтобы узнать погоду! ")


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_btn = types.KeyboardButton("Узнать погоду!")
    markup.add(item_btn)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Узнать погоду!":
        sent = bot.send_message(message.chat.id, "В каком городе?")
        bot.register_next_step_handler(sent, save_city)


@bot.message_handler(content_types='text')
def save_city(message):
    city = message.text

    config_dict = get_default_config()
    config_dict['language'] = 'ru'

    owm = OWM("7f87f117f943a0cf0171bc5c9692bcad")
    mgr = owm.weather_manager()

    observation = mgr.weather_at_place(city)

    w = observation.weather
    temp = w.temperature('celsius')['temp']
    status = w.detailed_status
    hum = w.humidity

    if temp >= 1.00 and temp <= 1.99 or temp <= -1.00 and temp >= -1.99:
        temp2 = ' градус, '
    elif temp >= 2.00 and temp <= 4.99 or temp <= -2.00 and temp >= -4.99:
        temp2 = ' градуса, '
    elif temp >= 5.00 or temp == 0 or temp <= -5.00:
        temp2 = ' градусов, '
    else:
        temp2 = ' градуса, '

    bot.send_message(message.chat.id, "В городе " + city + " сейчас " + str(temp) + temp2 + status + ", влажность воздуха " + str(hum) + "%")


bot.infinity_polling()