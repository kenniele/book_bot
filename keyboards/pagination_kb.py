from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from book.file_opened import book_in_dict

max_page = max(book_in_dict().keys())

def create_pagination_kb(current_page: int = 1) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text="<<" if current_page != 1 else chr(24), callback_data="prev"), \
                   InlineKeyboardButton(text=f"{current_page} / {max_page}", callback_data=f"{current_page}"),
                   InlineKeyboardButton(text=">>" if current_page != max_page else chr(24), callback_data="next"))
    return kb_builder.as_markup()