from django.core.management.base import BaseCommand
from datetime import datetime
from pycbrf import ExchangeRates
import telebot
from telebot import types
import sqlite3
from django.conf import settings


bot = telebot.TeleBot(settings.TOKEN_BOT)
name = None


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50),'
                'pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()
    mess_full = f'<b>Привет, {message.from_user.first_name} <u>{message.from_user.last_name}</u></b>'
    mess = f'<b>Привет, {message.from_user.first_name}</b>'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    usd_button = types.KeyboardButton('USD')
    markup.add(usd_button)
    if message.from_user.last_name is not None:
        bot.send_message(message.chat.id, mess_full, parse_mode='html')
    bot.send_message(message.chat.id, mess, parse_mode='html')
    bot.send_message(message.chat.id, "Сейчас вас зарегистрируем. Введите ваше имя")
    bot.register_next_step_handler(message, user_name)
    bot.send_message(message.chat.id, "После регистрации нажмите на кнопку USD, чтобы узнать курс доллара", reply_markup=markup)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, "Введите пароль")
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip()
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
    conn.commit()
    cur.close()
    conn.close()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Список пользователей", callback_data='users'))
    bot.send_message(message.chat.id, "Пользователь зарегистрирован", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def call_back(call):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    info = " "
    for el in users:
        info += f'Имя: {el[1]}, Пароль: {el[2]}\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    message_norm = message.text.strip().lower()

    if message_norm in ['usd']:
        rates = ExchangeRates(datetime.now())
        bot.send_message(message.chat.id, f"<b>Курс {message_norm.upper()} : "
                                          f"{float(rates[message_norm.upper()].rate)}</b>", parse_mode='html')
    if message.text == "Hello":
        bot.send_message(message.chat.id, "И тебе привет!", parse_mode='html')
    elif message.text == 'id':
        bot.send_message(message.chat.id, f'Твой ID: {message.from_user.id}', parse_mode='html')


@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    bot.send_message(message.chat.id, "Вау! Крутое фото!")


bot.polling(none_stop=True)






