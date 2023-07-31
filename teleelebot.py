import telebot

from config import API_TOKEN_TELEGRAM
from extensions import APIException, Converter

bot = telebot.TeleBot(API_TOKEN_TELEGRAM)

converter = Converter()


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    """
    Обработчик команд /help, /start
    """
    bot.reply_to(message, """Тут нужна инструкция по использованию""")


@bot.message_handler(commands=['values'])
def send_values(message):
    """
    Обработчик команды /values
    """
    bot.reply_to(message, '\n'.join([dd for dd in Converter.currency_type.values()]))


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    """
    Обработчик сообщения
    """
    try:
        tsyms, fsym, amount = message.text.split(' ')
    except ValueError:
        bot.reply_to(message, 'Сообщение не соответствует формату')
        return

    try:
        base_amount = converter.get_price(base=tsyms, quote=fsym, amount=amount)
    except APIException as e:
        bot.reply_to(message, str(e))
        return

    bot.reply_to(
        message,
        f'Цена {amount} {tsyms.upper()} по текущему курсу {fsym.upper()} составляет: {base_amount}'
    )


bot.infinity_polling()
