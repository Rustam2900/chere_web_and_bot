from django.core.management.base import BaseCommand
from django.conf import settings
import telebot
from bot.keyboards import get_languages

BOT_TOKEN = settings.BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id, text="Welcome Message, chose language", reply_markup=get_languages())


@bot.callback_query_handler(func=lambda x: x.data and x.data.startswith("lang"))
def query_get_languages(call):
    print(call.data)
    if call.data == "lang_uz":
        bot.send_message(chat_id=call.message.chat.id, text="Salom")
    elif call.data == "lang_ru":
        bot.send_message(chat_id=call.message.chat.id, text="Привет")


class Command(BaseCommand):

    def handle(self, *args, **options):
        bot.infinity_polling()