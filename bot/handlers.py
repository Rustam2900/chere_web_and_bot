from aiogram import Dispatcher, F, Bot
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, LabeledPrice
import environ
from django.contrib.auth.hashers import make_password

from bot.db import create_user_db, get_company_contacts, get_my_orders, login_user
from bot.keyboards import get_languages, get_user_types, get_registration_keyboard, get_user_contacts, \
    get_main_menu, get_confirm_button, get_registration_and_login_keyboard
from bot.states import LegalRegisterState, IndividualRegisterState, LoginStates
from bot.utils import default_languages, user_languages, introduction_template, calculate_total_water, \
    offer_text, order_text, local_user
from django.conf import settings
from aiogram.client.default import DefaultBotProperties

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(".env")
PROVIDER_TOKEN = env.str('PROVIDER_TOKEN')
dp = Dispatcher()
bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@dp.message(CommandStart())
async def welcome(message: Message):
    user_lang = user_languages.get(message.from_user.id, None)
    user_phone = local_user.get(message.from_user.id, None)
    if user_phone and user_lang:
        await message.answer_photo(
            photo="AgACAgIAAxkBAANIZtweuk4Z4BlQtDdS8jFgbuw6UBAAAvnaMRs33OBK3nbNtZNsdvMBAAMCAAN5AAM2BA",
            caption=introduction_template[user_lang], reply_markup=get_main_menu(user_lang))
    else:
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
    user_languages[user_id] = user_lang
    user = local_user.get(user_id, None)
    if user is None:
        await call.message.answer_photo(
            photo="AgACAgIAAxkBAANIZtweuk4Z4BlQtDdS8jFgbuw6UBAAAvnaMRs33OBK3nbNtZNsdvMBAAMCAAN5AAM2BA",
            caption=introduction_template[user_lang], reply_markup=get_registration_and_login_keyboard(user_lang))
    else:
        await call.message.answer_photo(
            photo="AgACAgIAAxkBAANIZtweuk4Z4BlQtDdS8jFgbuw6UBAAAvnaMRs33OBK3nbNtZNsdvMBAAMCAAN5AAM2BA",
            caption=introduction_template[user_lang], reply_markup=get_main_menu(user_lang))

@dp.callback_query(F.data == "registration")
async def reg_user_contact(call: CallbackQuery):
    user_id = call.from_user.id
    user_lang = user_languages[user_id]
    await call.message.answer(text=default_languages[user_lang]['select_user_type'],
                              reply_markup=get_user_types(user_lang))


@dp.callback_query(F.data == "login")
async def user_sign_in(call: CallbackQuery, state: FSMContext):
    user_lang = user_languages[call.from_user.id]
    await state.set_state(LoginStates.password)
    await call.message.answer(text=default_languages[user_lang]['sign_password'])


@dp.message(LoginStates.password)
async def sign_user_password(msg: Message, state: FSMContext):
    user_lang = user_languages[msg.from_user.id]
    await state.update_data(password=msg.text)
    await msg.answer(text=default_languages[user_lang]['contact'], reply_markup=get_user_contacts(user_lang))
    await state.set_state(LoginStates.phone)


@dp.message(LoginStates.phone)
async def sign_user_contact(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    user_lang = user_languages[user_id]
    state_data = await state.get_data()
    password = state_data['password']
    if message.text is None:
        phone = message.contact.phone_number
    else:
        phone = message.text
    user = await login_user(phone, password, user_id, username, user_lang)
    if user:
        local_user[message.from_user.id] = user.phone_number
        user_languages[user_id] = user.user_lang
        await message.answer(
            text=default_languages[user.user_lang]['successful_login'],
            reply_markup=get_main_menu(user.user_lang))
    else:
        await message.answer(
            text=default_languages[user_lang]['user_not_found'],
            reply_markup=get_registration_keyboard(user_lang))
    await state.clear()


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
    await message.answer(text=default_languages[user_lang]['employee_name'])
    await state.set_state(LegalRegisterState.employee_name)


@dp.message(LegalRegisterState.employee_name)
async def employee_name(message: Message, state: FSMContext):
    user_lang = user_languages[message.from_user.id]
    await state.update_data(employee_name=message.text)
    await message.answer(text=default_languages[user_lang]['company_contact'],
                         reply_markup=get_user_contacts(user_lang))
    await state.set_state(LegalRegisterState.company_contact)


@dp.message(LegalRegisterState.company_contact)
async def company_contact(message: Message, state: FSMContext):
    user_lang = user_languages[message.from_user.id]
    if message.text is None:
        await state.update_data(company_contact=message.contact.phone_number)
    else:
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
    await state.update_data(working_days=message.text)
    await message.answer(text=default_languages[user_lang]['password'])
    await state.set_state(LegalRegisterState.password)


@dp.message(LegalRegisterState.password)
async def working_days(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_lang = user_languages[user_id]
    state_data = await state.get_data()
    employees_count = int(state_data['employee_count'])
    durations_days = int(state_data['duration_days'])
    total_water = calculate_total_water(state_data['working_days'], employees_count, durations_days)
    data = {
        "full_name": state_data['employee_name'],
        "username": message.from_user.username,
        "password": make_password(message.text),
        "company_name": state_data['company_name'],
        "phone_number": state_data['company_contact'],
        "user_type": "legal",
        "user_lang": user_lang,
        "telegram_id": user_id,
        "tg_username": f"https://t.me/{message.from_user.username}",
    }
    await create_user_db(data)
    local_user[user_id] = state_data['company_contact']

    await message.answer(offer_text[user_lang].format(employees_count, durations_days, total_water),
                         reply_markup=get_confirm_button(user_lang))
    await state.clear()


@dp.message(IndividualRegisterState.full_name)
async def full_name(message: Message, state: FSMContext):
    user_lang = user_languages[message.from_user.id]
    await state.update_data(full_name=message.text)
    await message.answer(text=default_languages[user_lang]['password'])
    await state.set_state(IndividualRegisterState.password)


@dp.message(IndividualRegisterState.password)
async def get_individual_password(message: Message, state: FSMContext):
    user_lang = user_languages[message.from_user.id]
    await state.update_data(password=make_password(message.text))
    await message.answer(text=default_languages[user_lang]['contact'], reply_markup=get_user_contacts(user_lang))
    await state.set_state(IndividualRegisterState.contact)


@dp.message(IndividualRegisterState.contact)
async def contact(message: Message, state: FSMContext):
    user_lang = user_languages[message.from_user.id]
    data = await state.get_data()
    if message.text is None:
        data['phone_number'] = message.contact.phone_number
    else:
        data['phone_number'] = message.text
    data['user_type'] = 'individual'
    data['telegram_id'] = message.from_user.id
    data['username'] = message.from_user.username
    data['tg_username'] = f"https://t.me/{message.from_user.username}"
    data['user_lang'] = user_lang
    await create_user_db(data)
    await message.answer(text=default_languages[user_lang]['successful_registration'],
                         reply_markup=get_main_menu(user_lang))

    await state.clear()


@dp.message(F.text.in_(["↩️ Akkauntdan chiqish", "↩️ Выйти из аккаунта"]))
async def logout(message: Message):
    user_lang = user_languages[message.from_user.id]
    local_user.pop(message.from_user.id)
    await message.answer(
        text=default_languages[user_lang]['exit'],
        reply_markup=get_registration_and_login_keyboard(user_lang)
    )


@dp.message(F.text.in_(["⚙️ Настройки", "⚙️ Sozlamalar"]))
async def settings(message: Message):
    user_lang = user_languages[message.from_user.id]
    await message.answer(text=default_languages[user_lang]['select_language'], reply_markup=get_languages("setLang"))


@dp.callback_query(F.data.startswith("setLang"))
async def change_language(call: CallbackQuery):
    user_lang = call.data.split("_")[1]
    user_languages[call.from_user.id] = user_lang
    await call.message.answer(text=default_languages[user_lang]['successful_changed'],
                              reply_markup=get_main_menu(user_lang))


@dp.message(F.text.in_(["📲 Biz bilan bog'lanish", "📲 Связаться с нами"]))
async def contact_us(message: Message):
    contacts = await get_company_contacts()
    user_lang = user_languages[message.from_user.id]
    await message.answer(
        text=default_languages[user_lang]['contact_us_message'].format(
            contacts.address, contacts.phone_number1, contacts.phone_number2, contacts.work_time), )


@dp.message(F.text.in_(["📦 Mening buyurtmalarim", "📦 Мои заказы"]))
async def get_orders(message: Message):
    phone_number = local_user[message.from_user.id]
    user_lang = user_languages[message.from_user.id]
    my_orders = await get_my_orders(phone_number)
    msg = ""
    for order in my_orders:
        msg += f"{order_text[user_lang].format(order.order_number, order.status)}\n"
        msg += "----------------------------\n"
    await message.answer(text=f"{default_languages[user_lang]['order']}\n {msg}")


@dp.message(F.func(lambda msg: msg.web_app_data.data if msg.web_app_data else None))
async def get_btn(msg: Message):
    text = msg.web_app_data.data
    product_data = text.split("|")
    products = {}
    for i in range(len(product_data)):
        if len(product_data[i].split("/")) >= 3:
            title = product_data[i].split('/')[0]
            price = product_data[i].split('/')[1]
            quantity = product_data[i].split('/')[2]
            product = {
                "title": title,
                "price": int(price),
                "quantity": int(quantity)
            }
            products[i] = product
    await bot.send_invoice(
        chat_id=msg.chat.id,
        title="Оплата",
        need_name=True,
        need_phone_number=True,
        description="Оплата через Telegram bot",
        provider_token=PROVIDER_TOKEN,
        currency="UZS",
        payload="Ichki malumot",
        prices=[LabeledPrice(label=f"{product['title']}({product['quantity']})",
                             amount=(product['price'] * product['quantity']) * 100)
                for product in products.values()],
        max_tip_amount=50000000,  # Chayeviy
        suggested_tip_amounts=[100000, 300000, 500000, 600000],  # Chayeviy
        need_shipping_address=True,

    )


@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, ok=True)


@dp.message(F.func(lambda msg: msg.successful_payment if msg.successful_payment else None))
async def successful_payment(msg: Message):
    await msg.answer("To'lov uchun raxmat!")
