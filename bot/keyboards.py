from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_languages():

    keyboard = InlineKeyboardMarkup(row_width=2)
    uz_keyboard = InlineKeyboardButton(text='uz', callback_data='lang_uz')
    ru_keyboard = InlineKeyboardButton(text='ru', callback_data='lang_ru')
    keyboard.add(uz_keyboard, ru_keyboard)
    return keyboard