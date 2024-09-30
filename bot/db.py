from django.contrib.auth.hashers import check_password

from asgiref.sync import sync_to_async
from django.db import IntegrityError
from company.models import Contacts
from order.models import Order, CartItem
from product.models import Product
from users.models import CustomUser


@sync_to_async
def create_user_db(user_data):
    try:
        new_user = CustomUser.objects.create(**user_data)
        return new_user
    except IntegrityError:
        raise Exception("User already exists")


@sync_to_async
def login_user(phone, password, tg_id, tg_u, user_lang):
    user = CustomUser.objects.filter(phone_number=phone).last()
    if user and check_password(password, user.password):
        user.telegram_id = tg_id
        user.tg_username = f"https://t.me/{tg_u}"
        user.user_lang = user_lang
        user.save()
        return user
    else:
        return None


@sync_to_async
def get_user_db(telegram_id):
    try:
        user = CustomUser.objects.get()
        return user
    except CustomUser.DoesNotExist:
        return None


@sync_to_async
def get_company_contacts():
    contact = Contacts.objects.last()
    return contact


@sync_to_async
def get_my_orders(phone_number):
    return list(Order.objects.all().filter(phone_number=phone_number))

@sync_to_async
def create_item_db(t_id, p_id, p_quantity):
    user = CustomUser.objects.get(telegram_id=t_id)  # Получаем пользователя
    product = Product.objects.get(id=p_id)  # Получаем экземпляр продукта по его ID

    # Проверяем, что пользователь и продукт существуют
    if user and product:
        data = {
            "user": user,
            "product": product,  # Используем экземпляр продукта
            "quantity": p_quantity
        }
        item = CartItem.objects.create(**data)  # Создаем элемент корзины
        return item
    else:
        return None  # Возвращаем None, если пользователь или продукт не найдены


@sync_to_async
def create_order_from_cart(t_id, address, reminder_days):
    try:
        # Получаем пользователя
        user = CustomUser.objects.get(telegram_id=t_id)

        # Получаем элементы корзины пользователя
        cart_items = CartItem.objects.filter(user=user, is_visible=True)

        # Вычисляем общую стоимость
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Создаем заказ
        order = Order.objects.create(
            user=user,
            address=address,
            phone_number=user.phone_number,
            total_price=total_price,
            status=Order.OrderStatus.CREATED  # Устанавливаем статус заказа
        )
        user.reminder_days = reminder_days
        user.save()

        # Здесь можно добавить логику для связывания заказанных товаров с заказом, если нужно
        for item in cart_items:
            item.order = order  # Присваиваем заказ элементам корзины
            item.is_visible = False  # Помечаем элемент как невидимый, если это нужно
            item.save()  # Сохраняем изменения

        return order
    except CustomUser.DoesNotExist:
        print("Пользователь не найден.")
        return None