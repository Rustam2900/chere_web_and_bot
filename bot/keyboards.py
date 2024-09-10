from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils import default_languages


def cancel_button():
    btn = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Cancel", callback_data="cancel")],
    ])
    return btn

def get_languages():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="uz 🇺🇿", callback_data='lang_uz'),
         InlineKeyboardButton(text='ru 🇷🇺', callback_data='lang_ru')]])
    return keyboard


def get_registration_keyboard(user_language):
    registration_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=default_languages[user_language]['registration'], callback_data='registration')]])


    return registration_keyboard if registration_keyboard else []


def get_user_types(user_language):
    user_types_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=default_languages[user_language]['individual'], callback_data='individual'),
            InlineKeyboardButton(text=default_languages[user_language]['legal'], callback_data='legal')
        ]
    ])
    return user_types_keyboard if user_types_keyboard else []
