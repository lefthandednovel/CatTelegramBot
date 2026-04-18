import asyncio
import random
import aiohttp
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import Command
from services.cat_api import fetch_cat_urls, download_image_bytes
from services.keyboard import get_menu

router = Router()

@router.message(Command("cats"))
async def cmd_cats(message: Message):
    await message.answer("Сколько котиков?", reply_markup=get_menu())

@router.callback_query(F.data.startswith("cats_"))
async def cb_cats(callback: CallbackQuery):
    action = callback.data.split("_")[1]
    count = random.randint(1, 10) if action == "random" else int(action)
    
    await callback.message.delete()
    loading = await callback.message.answer(f"🔍 Ищу {count} котиков...")
    
    try:
        urls = await fetch_cat_urls(count)
        if not urls:
            await loading.edit_text("😿 Котики не найдены.")
            await callback.answer()
            return

        async with aiohttp.ClientSession() as session:
            # Скачиваем параллельно
            tasks = [download_image_bytes(session, url) for url in urls]
            images = await asyncio.gather(*tasks)

        await loading.delete()
        for i, img in enumerate(images, 1):
            if img:
                await callback.message.answer_photo(
                    photo=BufferedInputFile(img, filename=f"cat_{i}.jpg"),
                    caption=f"🐱 #{i}"
                )
                await asyncio.sleep(0.3)
    except Exception as e:
        await loading.edit_text(f"💥 Ошибка: {e}")
    finally:
        await callback.answer()  # Обязательно!