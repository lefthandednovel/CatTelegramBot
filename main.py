import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import start, cats

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

async def main():
    bot = Bot(token=BOT_TOKEN )
    
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start.router)
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