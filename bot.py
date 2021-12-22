# Импорт необходимых компонентов
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton
from settings import BOT_TOKEN
from bs4 import BeautifulSoup
import requests


# Функция которая соединяется с Телеграмом
def main():
    # Переменная которая позволит нам взаимодействовать с ботом
    my_bot = Updater(BOT_TOKEN)
    my_bot.dispatcher.add_handler(MessageHandler(Filters.contact, get_contact))  # Обработчик полученного телефона
    my_bot.dispatcher.add_handler(MessageHandler(Filters.contact, get_location))  # Обработчик полученной геопозиции
    my_bot.dispatcher.add_handler(CommandHandler('start', reply_start))  # Обработчик команды start
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Начать'), reply_start))  # Обработчик кнопки
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Анекдот'), get_anecdote))  # Обработчик кнопки
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))  # Обработчик текста
    my_bot.start_polling()  # Проверяет на наличие сообщений в Telegram
    my_bot.idle()  # Будет работать пока не остановить вручную


# Будет вызвано при отправке команды /start
def reply_start(bot, update):
    print('Отправлена команда /start.')  # Фиксируем работу в консоли для наглядности
    bot.message.reply_text(f'Successfully activated. Hello {bot.message.chat.first_name}!', reply_markup=get_keyboard())


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


# Создание клавиатуры и её разметки
def get_keyboard():
    contact_button = KeyboardButton('Отправить контакты', request_contact=True)
    location_button = KeyboardButton('Отправить геопозицию', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([['Анекдот', 'Начать'], [contact_button, location_button]], resize_keyboard=True)  # Добавляем кнопку
    return my_keyboard


# Функция печатает и отвечает на полученый контакт
def get_contact(bot, updater):
    print(bot.message.contact)
    bot.message.reply_text(f'{bot.message.chat.first_name}, мы получили ваш номер телефона!')


# Функция печатает и отвечает на полученую геопозиции
def get_location(bot, updater):
    print(bot.message.location)
    bot.message.reply_text(f'{bot.message.chat.first_name}, мы получили вашу местоположение!')


main()
