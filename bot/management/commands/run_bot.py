import asyncio

from aiogram import Bot, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from django.conf import settings
from django.core.management import BaseCommand

from bot.management.commands.commands import commands

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main():
    print("Starting bot...")
    from bot.handlers import dp
    await bot.set_my_commands(commands=commands)
    await dp.start_polling(bot)


class Command(BaseCommand):
    def handle(self, *args, **options):
        asyncio.run(main())
