from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.utils import default_languages


def get_languages():
    keyboard = InlineKeyboardMarkup(row_width=2)
    uz_keyboard = InlineKeyboardButton(text="uz 🇺🇿", callback_data='lang_uz')
    ru_keyboard = InlineKeyboardButton(text='ru 🇷🇺', callback_data='lang_ru')
    keyboard.add(uz_keyboard, ru_keyboard)
    return keyboard


def get_registration_keyboard(user_language):
    registration_keyboard = InlineKeyboardMarkup()

    registration_keyboard.add(
        InlineKeyboardButton(text=default_languages[user_language]['registration'], callback_data='registration'))

    return registration_keyboard if registration_keyboard else []


def get_user_types(user_language):
    user_types_keyboard = InlineKeyboardMarkup(row_width=2)
    user_types_keyboard.add(
        InlineKeyboardButton(text=default_languages[user_language]['individual'], callback_data='individual'))
    user_types_keyboard.add(
        InlineKeyboardButton(text=default_languages[user_language]['legal'], callback_data='legal'))

    return user_types_keyboard if user_types_keyboard else []
