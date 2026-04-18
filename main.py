import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import BOT_TOKEN

# Импортируем роутеры
from handlers import start_help, cats

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

async def main():
    # Настройка бота
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Создаём диспетчер и подключаем роутеры
    dp = Dispatcher()
    dp.include_router(start_help.router)
    dp.include_router(cats.router)
    
    logging.info(" Бот запущен...")
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logging.info("🛑 Остановка по Ctrl+C")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())