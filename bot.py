# Импорт необходимых компонентов
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from settings import BOT_TOKEN


# Будет вызвано при отправке команды /start
def reply_start(bot, update):
    print('Отправлена команда /start.')  # Фиксируем работу в консоли для наглядности
    bot.message.reply_text(f'Successfully activated.Hello {bot.message.chat.first_name}!')


# Будет отвечать темже сообщением что ему прислали
def parrot(bot, update):
    print(bot.message) # Дублируем сообщение в консоль для наглядности
    bot.message.reply_text(bot.message.text)  # Отправляем ответ пользователю


# Функция которая соединяется с Телеграмом
def main():
    # Переменная которая позволит нам взаимодействовать с ботом
    my_bot = Updater(BOT_TOKEN)
    my_bot.dispatcher.add_handler(CommandHandler('start', reply_start))  # Обработчик команды start

    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))

    my_bot.start_polling()  # Проверяет на наличие сообщений в Telegram
    my_bot.idle()  # Будет работать пока не остановить вручную


main()
