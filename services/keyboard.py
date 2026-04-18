from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        InlineKeyboardButton(text="Помощь", callback_data="help")
    ])