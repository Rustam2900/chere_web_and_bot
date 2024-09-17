from aiogram.fsm.state import State, StatesGroup
# state_storage = StateMemoryStorage()  # не используйте это в продакшене; переключитесь на redis

class LegalRegisterState(StatesGroup):
    company_name = State()
    employee_name = State()
    company_contact = State()
    employee_count = State()
    duration_days = State()
    working_days = State()
    password = State()

class IndividualRegisterState(StatesGroup):
    full_name = State()
    contact = State()
    password = State()
