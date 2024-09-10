from aiogram import Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from pyexpat.errors import messages
from rest_framework_simplejwt.utils import aware_utcnow

from bot.crud import create_user
from bot.keyboards import get_languages, get_user_types, get_registration_keyboard, cancel_button
from bot.states import LegalRegisterState, IndividualRegisterState
from bot.utils import default_languages, user_languages, all_languages, introduction_template

dp = Dispatcher()


@dp.message(CommandStart())
async def welcome(message: Message):
    msg = default_languages['welcome_message']
    await message.answer(msg, reply_markup=get_languages())


@dp.callback_query(F.data == "cancel")
async def cancel_callback(call: CallbackQuery, state: FSMContext):
    user_lang = user_languages[call.from_user.id]
    await state.clear()
    await call.message.answer("cancel", reply_markup=get_user_types(user_lang))


@dp.callback_query(F.data.startswith("lang"))
async def get_query_languages(call: CallbackQuery):
    user_id = call.from_user.id
    user_lang = call.data.split("_")[1]

    if user_lang in all_languages:
        user_languages[user_id] = user_lang
        # bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await call.message.answer_photo(
            photo="AgACAgIAAxkBAANIZtweuk4Z4BlQtDdS8jFgbuw6UBAAAvnaMRs33OBK3nbNtZNsdvMBAAMCAAN5AAM2BA",
            caption=introduction_template[user_lang], reply_markup=get_registration_keyboard(user_lang))
        print(user_languages)
    else:
        await call.message.answer(chat_id=user_id, text=default_languages['language_not_found'],
                                  reply_markup=get_languages())


@dp.callback_query(F.data == "registration")
async def user_select_type(call: CallbackQuery):
    user_id = call.from_user.id
    user_lang = user_languages[user_id]
    await call.message.answer(text=default_languages[user_lang]['select_user_type'],
                              reply_markup=get_user_types(user_lang))


@dp.callback_query(F.data.in_(['legal', 'individual']))
async def legal_individual_registration(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    user_lang = user_languages[user_id]
    if call.data == 'legal':
        await call.message.answer(text=default_languages[user_lang]['company_name'])
        await state.set_state(LegalRegisterState.company_name)
    elif call.data == 'individual':
        await call.message.answer(text=default_languages[user_lang]['full_name'])
        await state.set_state(IndividualRegisterState.full_name)


@dp.message(LegalRegisterState.company_name)
async def company_name(message: Message, state: FSMContext):
    user_lang = user_languages[message.from_user.id]
    await state.update_data(company_name=message.text)
    await message.answer(text=default_languages[user_lang]['employee_name'], reply_markup=cancel_button())
    await state.set_state(LegalRegisterState.employee_name)


@dp.message(LegalRegisterState.employee_name)
async def employee_name(message: Message, state: FSMContext):
    user_lang = user_languages[message.from_user.id]
    await state.update_data(employee_name=message.text)
    await message.answer(text=default_languages[user_lang]['company_contact'], reply_markup=cancel_button())
    await state.set_state(LegalRegisterState.company_contact)


@dp.message(LegalRegisterState.company_contact)
async def company_contact(message: Message, state: FSMContext):
    user_lang = user_languages[message.from_user.id]
    await state.update_data(company_contact=message.text)
    await message.answer(text=default_languages[user_lang]['employee_count'])
    await state.set_state(LegalRegisterState.employee_count)


@dp.message(LegalRegisterState.employee_count)
async def employee_count(message: Message, state: FSMContext):
    user_lang = user_languages[message.from_user.id]
    await state.update_data(employee_count=message.text)
    await message.answer(text=default_languages[user_lang]['duration_days'])
    await state.set_state(LegalRegisterState.duration_days)


@dp.message(LegalRegisterState.duration_days)
async def duration_days(message: Message, state: FSMContext):
    user_lang = user_languages[message.from_user.id]
    await state.update_data(duration_days=message.text)
    await message.answer(text=default_languages[user_lang]['working_days'])
    await state.set_state(LegalRegisterState.working_days)


@dp.message(LegalRegisterState.working_days)
async def working_days(message: Message, state: FSMContext):
    user_lang = user_languages[message.from_user.id]
    state_data = await state.get_data()
    data = {
        "full_name": state_data['full_name'],
        "user_name": message.from_user.username,
        "company_name": state_data['company_name'],
        "phone_number": state_data['company_contact'],
        "user_type": "legal",
        "telegram_id": message.from_user.id,
        "tg_username": f"https://t.me/{message.from_user.username}",
    }
    create_user(data)
    await message.answer(text=default_languages[user_lang]['successful_registration'])


@dp.message(IndividualRegisterState.full_name)
async def full_name(message: Message, state: FSMContext):
    user_lang = user_languages[message.from_user.id]
    await state.update_data(full_name=message.text)
    await message.answer(text=default_languages[user_lang]['company_contact'], reply_markup=cancel_button())
    await state.set_state(IndividualRegisterState.contact)


@dp.message(IndividualRegisterState.contact)
async def contact(message: Message, state: FSMContext):
    user_lang = user_languages[message.from_user.id]
    data = await state.get_data()
    data['phone_number'] = message.text
    data['user_type'] = 'individual'
    data['telegram_id'] = message.from_user.id
    data['username'] = message.from_user.username
    data['tg_username'] = f"https://t.me/{message.from_user.username}"
    await create_user(data)
    await message.answer(text=default_languages[user_lang]['successful_registration'])
