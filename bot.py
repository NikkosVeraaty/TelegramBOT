# Импорт необходимых компонентов
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from handlers import *
from settings import BOT_TOKEN
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


# Функция которая соединяется с Телеграмом
def main():
    # Переменная которая позволит нам взаимодействовать с ботом
    my_bot = Updater(BOT_TOKEN)

    logging.info('Start bot')  # Добавление свое инфо сообщение

    my_bot.dispatcher.add_handler(MessageHandler(Filters.contact, get_contact))  # Обработчик полученного телефона
    my_bot.dispatcher.add_handler(MessageHandler(Filters.contact, get_location))  # Обработчик полученной геопозиции
    my_bot.dispatcher.add_handler(CommandHandler('start', reply_start))  # Обработчик команды start
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Начать'), reply_start))  # Обработчик кнопки
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Анекдот'), get_anecdote))  # Обработчик кнопки

    my_bot.dispatcher.add_handler(
        ConversationHandler(entry_points=[MessageHandler(Filters.regex('Заполнить анкету'), anketa_start)],
                            states={'user_name': [MessageHandler(Filters.text, anketa_get_name)],
                                    'user_age': [MessageHandler(Filters.text, anketa_get_age)],
                                    'evaluation': [MessageHandler(Filters.regex('1|2|3|4|5'), anketa_get_evaluation)],
                                    'comment': [MessageHandler(Filters.regex('Пропустить'), anketa_exit_comment),
                                                MessageHandler(Filters.text, anketa_comment)]},
                            fallbacks=[MessageHandler(
                                Filters.text | Filters.video | Filters.photo | Filters.document, dontknow)]
                            )
    )

    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))  # Обработчик текста
    my_bot.start_polling()  # Проверяет на наличие сообщений в Telegram
    my_bot.idle()  # Будет работать пока не остановить вручную


if __name__ == '__main__':
    main()
