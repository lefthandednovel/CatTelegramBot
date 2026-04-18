from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from utils.texts import load_text
from config import TEXTS_DIR

router = Router() 


@router.message(Command("start"))
async def send_static_text(event: Message):
    text = load_text("start.txt") 
    await event.answer(text)