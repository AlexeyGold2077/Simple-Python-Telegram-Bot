from secret import TOKEN
import telebot
from telebot import types
import requests

# bot
bot = telebot.TeleBot(TOKEN)

# binance api
url = 'https://api.binance.com/api/v3/ticker/price'
params = {'symbol': 'BTCUSDT'}
resp = requests.get(url, params=params)


@bot.message_handler(commands=['start'])
def handle_command_start(message):
    button_btc = types.InlineKeyboardButton('BTC', callback_data='button_btc')
    button_eth = types.InlineKeyboardButton('ETH', callback_data='button_eth')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button_btc)
    keyboard.add(button_eth)

    bot.send_message(message.from_user.id, 'Курс чего вы хотите узнать?', reply_markup=keyboard)


@bot.message_handler(content_types='text')
def handle_text(message):
    bot.send_message(message.from_user.id, 'Нажмите /start для начала.')


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'button_btc':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        resp = requests.get(url, params={'symbol': 'BTCUSDT'})
        bot.send_message(callback.message.chat.id, f"BTC price: {resp.json()['price']}")
    elif callback.data == 'button_eth':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        resp = requests.get(url, params={'symbol': 'ETHUSDT'})
        bot.send_message(callback.message.chat.id, f"ETH price: {resp.json()['price']}")


bot.polling(none_stop=True, interval=0)