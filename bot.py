# Импорт необходимых компонентов
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers import *
from settings import BOT_TOKEN



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


if __name__ == '__main__':
    main()
