all_languages = ['ru', 'uz']

default_languages = {
    "language_not_found": "Siz toʻgʻri tilni tanlamadingiz!\n"
                          "Вы не выбрали правильный язык!",
    "welcome_message": "Salom, botimizga xush kelibsiz!\n"
                       "Quyidagi tillardan birini tanlang!\n\n"
                       "Здравствуйте, добро пожаловать в наш бот!\n"
                       "Выберите один из языков ниже!",

    "uz": {
        "full_name": "To'liq ismingizni kiriting",
        "individual": "Jismoniy shaxs",
        "legal": "Yuridik shaxs",
        "select_user_type": "Foydalanuvchi turini tanlang",
        "registration": "Ro'yxatdan o'tish",
        "company_name": "Kampaniya nomini kiriting",
        "employee_name": "Kampaniya xodimi ism familiyasini kiriting",
        "employee_count": "Kampaniyada ishchilar sonini kiriting",
        "company_contact": "Kampaniya telefon raqamini kiriting",
        "working_days": "Kampaniyadagi ish kuni sonini kiriting",
        "duration_days": "Qancha vaqt mobaynida yetkazib berib turishimizni hohlaysiz?",
        "successful_registration": "Muvaffaqiyatli ro'yxatdan o'tildi",
        "contact": "Telefon raqamingizni kiriting",
        "share_contact": "Kantaktni bo'lishish",
        "password": "Akkountingiz uchun parol kiriting",
        "web_app": "📎 Veb ilova",
        "settings": "⚙️ Sozlamalar",
        "contact_us": "📲 Biz bilan bog'lanish",
        "my_orders": "📦 Mening buyurtmalarim",
        "create_order": "Buyurtma berish",
        "cancel": "Bekor qilish",
        "select_language": "Tilni tanlang!",
        "successful_changed": "Muvaffaqiyatli o'zgartirildi",
        "contact_us_message": "Bizning manzil:\n{}\n\n"
                              "Biz bilan bog'laning:\n{}\n{}\n\n"
                              "Murojaat vaqti:\n{}"

    },

    "ru": {
        "full_name": "Введите свое полное имя",
        "individual": "Физическое лицо",
        "legal": "Юридическое лицо",
        "select_user_type": "Выберите тип пользователя",
        "registration": "Зарегистрироваться",
        "company_name": "Введите название кампании",
        "employee_name": "Введите имя и фамилию сотрудника кампании.",
        "employee_count": "Введите количество работников в кампании.",
        "company_contact": "Введите номер телефона кампании",
        "working_days": "Введите количество рабочих дней в кампании",
        "duration_days": "Как долго вы хотите, чтобы мы доставили?",
        "successful_registration": "Успешная регистрация",
        "contact": "Введите свой номер телефона",
        "share_contact": "Поделиться контактом",
        "password": "Введите пароль для вашей учетной записи",
        "web_app": "📎 Веб-приложение",
        "settings": "⚙️ Настройки",
        "contact_us": "📲 Связаться с нами",
        "my_orders": "📦 Мои заказы",
        "create_order": "Сделать заказ",
        "cancel": "Отменить",
        "select_language": "Выберите язык!",
        "successful_changed": "Успешно изменено",
        "contact_us_message": "Наш адрес:\n{}\n\n"
                              "Связаться с нами:\n{}\n{}\n\n"
                              "Время подачи заявки:\n{}"
    }
}

user_languages = {}
user_contacts = {}
introduction_template = {
    'ru':
        """
    💧Chere Water Company представляет <a href="https://t.me/chere_water_bot">Chere Water</a> 💧

    Решите все вопросы, связанные с водой Chere! 🚰

    Что может сделать бот?
    - Заказ воды
    - Знать о последних тарифах на воду
    - Проверка расчетов
    - Будьте в курсе эксклюзивных скидок и акций
    - Вопросы и помощь
    🌐 ChereBot - легкий и быстрый сервис!

    🏠 Оставайтесь дома и пользуйтесь уникальными услугами!

    🟢 Присоединяйтесь прямо сейчас: <a href="https://t.me/chere_water_bot">Chere Water</a>
    ✉️  Телеграм канал: <a href="https://t.me/chere_water_bot">Chere Water</a>

    Chere - Чистая вода, Здоровая жизнь!
    """,

    "uz":

        """
    💧 Chere Suv Kompaniyasi <a href="https://t.me/chere_water_bot">Chere Water</a> ni taqdim etadi 💧
    
    Chere suvi bilan bog'liq barcha masalalaringizni hal qiling! 🚰
    
    Bot nimalarni qila oladi?
    - Suv buyurtma qilish
    - So'nggi suv tariflarini bilish
    - Hisob-kitoblarni tekshirish
    - Eksklyuziv chegirmalar va aksiyalar haqida xabardor bo'lish
    - Savollar va yordam
    🌐 ChereBot – oson va tezkor xizmat! 
    
    🏠 Uyda qolib unikal xizmatlardan foydalaning!
    
    🟢 Hoziroq qo'shiling: <a href="https://t.me/chere_water_bot">Chere Water</a>
    ✉️ Telegram kanal: <a href="https://t.me/chere_water_bot">Chere Water</a>
    
    Chere - Sof Suv, Sog‘lom Hayot!

    """
}

bot_description = """
Bu bot Nima qila qila oladi?

💦 Ushbu bot Chere sof ichimlik suvini uydan turib istalgan vaqtda buyurtma qilishingiz va xizmat turlaridan foydalanishingiz uchun yaratilgan 💦

- - - - - - - - - - - - - - - - - - - - - - - - - 

💦 Этот бот создан для того, чтобы вы могли заказывать чистую питьевую воду Chere в любое время из дома и пользоваться услугами 💦
"""

offer_text = {
    "ru":
        "Сотрудники: {}\n"
        "День непрерывности: {}\n"
        "Мы рекомендуем вашим работникам {} бутылок с водой по 20 л.\n",
    "uz":
        """
    Xodim: {}
    Davomiylik kuni: {}
    Xodimlaringizga {} x 20 litrli suv idishlarini tavsiya qilamiz.
        """
}


def calculate_total_water(week_days, employee_count, durations_days):
    available_days = int(durations_days) // int(week_days) + int(durations_days) % int(week_days)
    total_water = available_days * int(employee_count) * 2
    return total_water // 20
