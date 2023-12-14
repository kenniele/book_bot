from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.database import get_info

def create_bookmarks_kb(data: list[str], user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder() 
    buttons = [InlineKeyboardButton(text=text, callback_data=f"{text.split(' - ')[0]}edit") for text in data]
    kb.row(*buttons, width=1)
    kb.row(*[InlineKeyboardButton(text="❌ Редактировать", callback_data="editor"), InlineKeyboardButton(text="Отменить", callback_data="cancel_in_bookmark")])
    return kb.as_markup()

def create_editor_kb(data: list[str], user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text="❌ " + text, callback_data=f"{text.split(' - ')[0]}del") for text in data] + [InlineKeyboardButton(text="Отменить", callback_data="cancel_in_deleter")]
    kb.row(*buttons, width=1)
    return kb.as_markup()