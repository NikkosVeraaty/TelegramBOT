# Импорт необходимых компонентов
from bs4 import BeautifulSoup
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler

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


def anketa_start(bot, update):
    bot.message.reply_text('Как вас зовут?', reply_markup=ReplyKeyboardRemove())  # Вопрос и убираем основную клавиатуру
    return 'user_name'  # Ключ для определения след.шага


def anketa_get_name(bot, update):
    update.user_data['name'] = bot.message.text  # Временно сохраняем ответ
    bot.message.reply_text('Сколько вам лет?')  # Задаем вопрос
    return 'user_age'  # Ключ для определения следующего шага


def anketa_get_age(bot, update):
    update.user_data['age'] = bot.message.text  # Временно сохраняем ответ
    reply_keyboard = [['1', '2', '3', '4', '5']]  # Создаем клавиатуру
    bot.message.reply_text(
        'Оцените анекдот от 1 до 5',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True))  # При нажатии клавиатура исчезает
    return 'evaluation'  # Ключ для определения след.шага


def anketa_get_evaluation(bot, update):
    update.user_data['evaluation'] = bot.message.text  # Временно сохраняем ответ
    reply_keyboard = [['Пропустить']]  # Создаем клавиатуру
    bot.message.reply_text('Напишите отзыв или пропустите этот шаг.',
                           reply_markup=ReplyKeyboardMarkup(
                               reply_keyboard, one_time_keyboard=True, resize_keyboard=True))  # Клавиатура исчезает
    return 'comment'  # ключ для следующего шага


def anketa_exit_comment(bot, update):
    update.user_data['comment'] = bot.message.text  # Временно сохраняем ответ
    text = f"""Результат опроса:
    <b>Имя:</b> {update.user_data['name']}
    <b>Возраст:</b> {update.user_data['age']}
    <b>Оценка:</b> {update.user_data['evaluation']}"""
    bot.message.reply_text(text, parse_mode=ParseMode.HTML)  # текстовое сообщение с форматированием HTML
    bot.message.reply_text('Спасибо!', reply_markup=get_keyboard())  # отправляем сообщение и возвращаем основную клавиатуру
    return ConversationHandler.END  # выходим из диалога


def anketa_comment(bot, update):
    update.user_data['comment'] = bot.message.text  # Временно сохраняем ответ
    text = f"""Результат опроса:
    <b>Имя:</b> {update.user_data['name']}
    <b>Возраст:</b> {update.user_data['age']}
    <b>Оценка:</b> {update.user_data['evaluation']}
    <b>Коментарий:</b> {update.user_data['comment']}"""
    bot.message.reply_text(text, parse_mode=ParseMode.HTML)  # текстовое сообщение с форматированием HTML
    bot.message.reply_text('Спасибо вам за комментарий!', reply_markup=get_keyboard())
    return ConversationHandler.END  # выходим из диалога


def dontknow(bot, update):
    bot.message.reply_text('Я вас не понимаю, выберите оценку на клавиатуре.')