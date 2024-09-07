from telebot.states import State, StatesGroup

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