import requests
from time import sleep  
from bs4 import BeautifulSoup
import datetime
import telebot
from telebot import types
import csv
import json
from pathlib import Path

class ForMoney:

    URL_money = "https://finance.rambler.ru/currencies/"

    
    def get_html(self, url, perams = None):
        html = requests.get(url, params)
        return html

    def get_money(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', 'currency-block__row')

        for item in items:
            item_date = item.find('div', class_='currency-block__marketplace-title')
            item_value = item.find('div', class_='currency-block__marketplace-value')



class BotHandler:

    URL = "https://www.bontour.ru/tours/tours-to-europe/?PAGEN_1=1"
    operData = []
    left_menu = []
    def get_html(self, url, params = None): #получаем доступ к сайту()потом и код пбудем получать
        r = requests.get(url, params)
        return r

    def get_content(self, html): #парсер основной инфы
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('tr') #ищем на сайте тег tr

        self.operData = []        
        
        for item in items: #в теге tr ищем что-то
            item_tdid3 = item.find('td', class_ = 'tdid3')
            item_tdid4 = item.find('td', class_ = 'tdid4')
            item_tdid5 = item.find('td', class_ = 'tdid5')

            if item_tdid3 != None: #в td были ноны поэтому проифал
                self.operData.append({ #добавляю все данные в виде словарей в массив
                    'tour_name': item_tdid3.get_text(), #гет текст выдает только текст
                    'tour_waybill': item_tdid4.get_text(),
                    'tour_price': item_tdid5.get_text()
                })

        for i in range(len(self.operData)):
            print(self.operData[i], '\n')
        
        return self.operData

    def get_left_menu(self, html): #парсер левой части страницы(направления туров)
        soup = BeautifulSoup(html, 'html.parser')
        items2 = soup.find_all('div', class_= 'leftmenu')
        self.left_menu = []

        for item2 in items2:
            item_li = item2.find_all('a')

            for item22 in item_li:
                self.left_menu.append({
                    'catalog_item': item22.get_text(),
                    'catalog_href': item22.get('href') #выдают саму ссылку из а-href
                    })

        for i in range(len(self.left_menu)):
            print(self.left_menu[i], '\n')

        return self.left_menu

    def parse(self):
        html = self.get_html(self.URL)
        print(html.status_code) #если 200 код то все норм, если 505 или что-то в этом роде то нет
        if html.status_code == 200: #тут гет запросы обычные, поэтому почти всегда будет 200
            print('Good connection') #но на всякий случай надо прочекать все
        else:
            print('Error')

        return self.get_content(html.text)

    def parse_leftmenu(self):
        html = self.get_html(self.URL)
        print(html.status_code)
        return self.get_left_menu(html.text)




#Работа с ботом

token = "сюда ставь токен своего бота"
bot = telebot.TeleBot(token)
parser_tours = BotHandler()  
parser_tours1 = BotHandler() 
data_tours = parser_tours.parse().copy() #выведи эту инфу просто и все
data_menu = parser_tours1.parse_leftmenu().copy()

print('TESTING')

global clientData
clientData = dict()

# print(data_menu)

@bot.message_handler(commands=['start'])
def start_message(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('/start', '/stop')
    user_markup.row('Каталог наших туров')
    user_markup.row('Все туры')
    user_markup.row('Перейти на наш сайт')
    user_markup.row('Курс валют')
    user_markup.row('Контакты', 'Забронировать')
    bot.send_message(message.from_user.id, f'Приветствую, {message.from_user.first_name}! \nМеня зовут Туров! И я помогу тебе в выборе твоего идеального путешествия!', reply_markup=user_markup)

@bot.message_handler(commands=['stop'])
def start_message(message):
    hide_markup = telebot.types.ReplyKeyboardMarkup()
    bot.send_message(message.from_user.id, f'До скорой встречи, {message.from_user.first_name}', reply_markup=hide_markup)

@bot.message_handler(content_types = ['text'])
def get_text_messages(message):
    if message.text == 'Все туры':
        for i in range(len(data_tours)):
            bot.send_message(message.from_user.id, data_tours[i]['tour_name'] + 2 * '\n' + 'Цена: ' + data_tours[i]['tour_price'])
    elif message.text.lower() == 'каталог' or message.text == 'Каталог наших туров':
        for i in range(len(data_menu)):
            bot.send_message(message.from_user.id, data_menu[i]['catalog_item'])
    elif message.text.lower() == 'сайт' or message.text == 'Перейти на наш сайт':
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Буду рад увидеть тебя на нашем сайте", url="https://www.bontour.ru/tours/europe/")
        keyboard.add(url_button)
        bot.send_message(message.chat.id, "Нажимай на кнопку БонТур.", reply_markup=keyboard)
    elif message.text.lower() == 'курс валют' or message.text == 'Курс валют':
        bot.send_message(message.chat.id, "Евро - 79.62 руб. Доллар - 70.86 руб.")
    elif message.text == 'Контакты':
        bot.send_message(message.chat.id, "ОФИС В МОСКВЕ +7 (495) 640-62-24 \n САНКТ-ПЕТЕРБУРГ +7 (812) 335-99-90")
    elif message.text.lower() == 'оставить заявку' or message.text == 'Забронировать':
        msg = bot.send_message(message.chat.id, f'{message.from_user.first_name} {message.from_user.last_name}, оставь свой номер телефона и с тобой скоро созвонится наш оператор!')
        bot.register_next_step_handler(msg, phone_num)

def phone_num(message):
    global number
    number = message.text
    print("Номер ", number)
    msg = bot.send_message(message.chat.id, f'{message.from_user.first_name}, напиши еще тур, который тебе больше всего интересен.')
    bot.register_next_step_handler(msg, tour_num)

def tour_num(message):
    global tour
    tour = message.text
    print(tour)
    msg = bot.send_message(message.chat.id, f'Введи серию и номер своего паспорта')
    bot.register_next_step_handler(msg, pas_num)

def pas_num(message):
    global pas
    pas = message.text
    print(pas)
    msg = bot.send_message(message.chat.id, f'Отлично, давай подтвердим данные?')
    bot.register_next_step_handler(msg, final)

def final(message):
    bot.send_message(message.chat.id, f'Тебя зовут {message.from_user.first_name} {message.from_user.last_name} \n Твой телефон {number} \n Выбранный тур {tour} \n Паспорт {pas} \n \n Данные отправлены! Жди звонка от менеджера для окончательного подтверждения и оплаты.' )
    key = f'{message.from_user.first_name} {message.from_user.last_name}'
    
    # tempData = clientData[f'{message.from_user.first_name} {message.from_user.last_name}'].copy()

    path = Path('users.json')
    clientData = json.loads(path.read_text(encoding='utf-8'))
    print(clientData)
    clientData[f'{message.from_user.first_name} {message.from_user.last_name} {message.from_user.username}'] = []
    clientData[f'{message.from_user.first_name} {message.from_user.last_name} {message.from_user.username}'].append(number)
    clientData[f'{message.from_user.first_name} {message.from_user.last_name} {message.from_user.username}'].append(tour)
    clientData[f'{message.from_user.first_name} {message.from_user.last_name} {message.from_user.username}'].append(pas)
    path.write_text(json.dumps(clientData), encoding='utf-8')
    print(clientData)

    # with open('users.json', 'w') as f:
    #     # json.dumps(clientData, f)
    #     f.write(json.dumps(clientData))

bot.polling(none_stop = True, interval = 0)


