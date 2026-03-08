import asyncio
import os
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv

from handlers import start, profile, vacancies


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


async def main():

    if not TOKEN:
        sys.exit("❌ BOT_TOKEN не найден")

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(vacancies.router)

    logging.info("🚀 Бот запущен")

    await dp.start_polling(bot)


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    asyncio.run(main())