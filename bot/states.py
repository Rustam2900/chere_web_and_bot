from telebot.states import State, StatesGroup
from telebot.storage import StateMemoryStorage
state_storage = StateMemoryStorage()  # не используйте это в продакшене; переключитесь на redis

class LegalRegisterState(StatesGroup):
    company_name = State()
    employee_name = State()
    company_contact = State()
    employee_count = State()
    duration_days = State()
    working_days = State()

class IndividualRegisterState(StatesGroup):
    full_name = State()
    contact = State()