from django.core.management.base import BaseCommand
from django.conf import settings
import telebot
from telebot.types import InputFile, InputMediaPhoto

from bot.keyboards import get_languages, get_registration_keyboard, get_user_types
from bot.states import LegalRegisterState, IndividualRegisterState
from bot.utils import default_languages, all_languages, user_languages, introduction_template, bot_description

BOT_TOKEN = settings.BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)
bot.set_my_description(bot_description)

@bot.message_handler(commands=['start'])
def welcome(message):
    msg = default_languages['welcome_message']
    bot.send_message(chat_id=message.chat.id, text=msg, reply_markup=get_languages())


@bot.callback_query_handler(func=lambda x: x.data and x.data.startswith("lang"))
def query_get_languages(call):
    user_id = call.from_user.id
    user_lang = call.data.split("_")[1]

    if user_lang in all_languages:
        user_languages[user_id] = user_lang
        # bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_photo(chat_id=user_id,
                       photo="AgACAgIAAxkBAANIZtweuk4Z4BlQtDdS8jFgbuw6UBAAAvnaMRs33OBK3nbNtZNsdvMBAAMCAAN5AAM2BA",
                       caption=introduction_template[user_lang], reply_markup=get_registration_keyboard(user_lang),
                       parse_mode='HTML')
        print(user_languages)
    else:
        bot.send_message(chat_id=user_id, text=default_languages['language_not_found'], reply_markup=get_languages())


@bot.callback_query_handler(func=lambda call: call.data == 'registration')
def user_registration(call):
    user_id = call.from_user.id
    user_lang = user_languages[user_id]
    bot.send_message(chat_id=user_id, text=default_languages[user_lang]["select_user_type"],
                     reply_markup=get_user_types(user_lang))


@bot.callback_query_handler(func=lambda call: call.data in ['legal', 'individual'])
def legal_individual_registration(call):
    user_id = call.from_user.id
    user_lang = user_languages[user_id]
    if call.data == 'legal':
        bot.send_message(chat_id=user_id, text=default_languages[user_lang]['company_name'],)
        bot.set_state(user_id=user_id, state=LegalRegisterState.company_name)
    elif call.data == 'individual':
        bot.send_message(chat_id=user_id, text=default_languages[user_lang]['full_name'],)
        bot.set_state(user_id=user_id, state=IndividualRegisterState.full_name)


# @bot.message_handler(content_types=['photo'])
# def handle_photo(message):
#     # Rasmning eng yuqori sifatli versiyasini olish
#     photo_id = message.photo[-1].file_id
#
#     bot.reply_to(message, text=f"Rasm qabul qilindi!\n"
#                                f"{photo_id}")


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Started....")
        bot.infinity_polling()
