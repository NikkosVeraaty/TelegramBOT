# Импорт необходимых компонентов
from bs4 import BeautifulSoup
from utility import get_keyboard
import requests


# Будет вызвано при отправке команды /start
def reply_start(bot, update):
    print('Отправлена команда /start.')  # Фиксируем работу в консоли для наглядности
    bot.message.reply_text(f'Successfully activated. Hello {bot.message.chat.first_name}!',
                           reply_markup=get_keyboard())


def get_anecdote(bot, update):
    receive = requests.get('http://anekdotme.ru/random')  # Отправляем запрос к странице
    page = BeautifulSoup(receive.text, "html.parser")  # HTML-parser получаем текст страницы
    find = page.select('.anekdot_text')  # Получаем класс anekdot_text
    for text in find:
        page = (text.getText().strip())  # Из класса anekdote_text получаем текст и убираем пробелы по бокам
    bot.message.reply_text(page)  # Отправляем один анекдот


# Будет отвечать темже сообщением что ему прислали
def parrot(bot, update):
    print(bot.message.text)  # Дублируем сообщение в консоль для наглядности
    bot.message.reply_text(bot.message.text)  # Отправляем ответ пользователю


# Функция печатает и отвечает на полученый контакт
def get_contact(bot, updater):
    print(bot.message.contact)
    bot.message.reply_text(f'{bot.message.chat.first_name}, мы получили ваш номер телефона!')


# Функция печатает и отвечает на полученую геопозиции
def get_location(bot, updater):
    print(bot.message.location)
    bot.message.reply_text(f'{bot.message.chat.first_name}, мы получили вашу местоположение!')