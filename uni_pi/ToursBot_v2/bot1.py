import requests
from time import sleep  
from bs4 import BeautifulSoup
import datetime
import telebot
from telebot import types
import csv
import json



token = "999490022:AAFLTlXMd0hHnTZJD4PulTdQy1EOrir79Nk"
bot = telebot.TeleBot(token)

# data_menu = ['Gleb Shevchenko', 89855574067, 'Тур ВА-8', 'Паспорт 3645 234589']

@bot.message_handler(commands=['start'])
def start_message(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('Войти')
    bot.send_message(message.from_user.id, f'B2B BOTS', reply_markup=user_markup)

@bot.message_handler(content_types = ['text'])
def get_text_messages(message):
    if message.text == 'Войти':
        msg = bot.send_message(message.from_user.id, f'Введи логин')
        bot.register_next_step_handler(msg, login)
    elif message.text == 'База клиентов':
    	with open('users.json') as users_file:
    		users = json.load(users_file)
    	print(users)
    	fio = list(users.keys())
    	info = list(users.values())
    	for i in range(len(fio)):
       		bot.send_message(message.from_user.id, f'{fio[i]} {info[i]}')

def login(message):
	global login
	print(login)
	login = message.text
	msg = bot.send_message(message.chat.id, f'Логин подтвержден. Введи пароль.')
	bot.register_next_step_handler(msg, passw)

def passw(message):
	global pas
	global users
	pas = message.text
	print(pas)
	msg = bot.send_message(message.chat.id, f'Доступ разрешен')
	with open('users.json') as users_file:
		users = json.load(users_file)
	bot.register_next_step_handler(msg, data)

def data(message):
	user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
	user_markup.row('/start', '/stop')
	user_markup.row('База клиентов')
	bot.send_message(message.from_user.id, f'Добро пожаловать', reply_markup=user_markup)

bot.polling(none_stop = True, interval = 0)