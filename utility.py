# Импорт необходимых компонентов
from telegram import ReplyKeyboardMarkup, KeyboardButton


# Создание клавиатуры и её разметки
def get_keyboard():
    contact_button = KeyboardButton('Отправить контакты', request_contact=True)
    location_button = KeyboardButton('Отправить геопозицию', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([['Анекдот', 'Начать'],
                                       [contact_button, location_button]], resize_keyboard=True)  # Добавляем кнопку
    return my_keyboard