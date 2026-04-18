import asyncio
import random
import aiohttp
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import Command
from services.cat_api import fetch_cat_urls, download_image_bytes
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

router = Router()

class CatsState(StatesGroup):
    waiting_for_num = State()

@router.message(Command("cats"))
async def cmd_cats_start(message: Message, state: FSMContext):
    await message.answer("Сколько котиков отправить? (1-10)")
    await state.set_state(CatsState.waiting_for_num)
    

@router.message(CatsState.waiting_for_num)
async def process_num(message: Message, state: FSMContext):

    if not message.text:
        await message.answer("Напиши число циферками")
        return
    
    try:
        count = int(message.text)
    except ValueError:
        await message.answer("Напиши число циферками")
        return
    
    if not (1 <= count <= 10):
        await message.answer("Число должно быть от 1 до 10 >_<\nВведи ещё раз")
        return
    
    await state.clear()

    if count > 1:
        loading = await message.answer(f"Ищу {count} котиков, мяу")
    else:
        loading = await message.answer(f"Ищу {count} котика, мяу")
    
    try:
        urls = await fetch_cat_urls(count)
        print(f"DEBUG: Получены URL: {urls}") 
        print(f"DEBUG: Количество URL: {len(urls)}")

        if not urls:
            await loading.edit_text("API не дал картинок, мяу(")
            return
        
        async with aiohttp.ClientSession() as session:
            tasks = [download_image_bytes(session, url) for url in urls]
            images = await asyncio.gather(*tasks)

            print(f"DEBUG: Картинки скачаны. Всего: {len(images)}")
            print(f"DEBUG: Тип данных первой картинки: {type(images[0]) if images else 'Пусто'}")


        await loading.delete()
        for i, img_bytes in enumerate(images, start=1):
            if img_bytes: 
                photo_file = BufferedInputFile(img_bytes, filename=f"cat_{i}.jpg")
                await message.answer_photo(
                    photo=photo_file,
                    caption=f"🐱 Котик #{i}"
                )
                await asyncio.sleep(0.3)
            else:
                await message.answer(f"❌ Котик #{i} не скачался, пропускаем.")

    except Exception as e:
        await message.answer(f"💥 Произошла ошибка: {e}")

