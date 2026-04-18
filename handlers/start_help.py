from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from utils.texts import load_text

router = Router()  # ← Каждый файл создаёт свой роутер

@router.message(Command("start", "help") | F.text == "📖 Помощь")
async def send_static_text(event: Message | CallbackQuery):
    text = load_text("help.txt") if isinstance(event, Message) and "/help" in event.text else load_text("start.txt")
    
    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text)
        await event.answer()
    else:
        await event.answer(text)