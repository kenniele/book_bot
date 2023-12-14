from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import LEXICON_RU
from keyboards import bookmarks_kb, main_menu_kb, pagination_kb
from book.file_opened import book_in_dict
from database.database import fill_database, get_info
from filters import filters

router = Router()

@router.message(CommandStart())
async def process_start_message(message: Message) -> None:
    if get_info().get(message.from_user.id) is None:
        get_info()[message.from_user.id] = {"current_page": 1}
    await message.answer(text=LEXICON_RU["/start"])

@router.message(Command("help"))
async def process_help_message(message: Message) -> None:
    await message.answer(text=LEXICON_RU["/help"])

@router.message(Command("beginning"))
async def process_beginning_message(message: Message) -> None:
    get_info()[message.from_user.id].update({"current_page": 1})
    fill_database()
    await message.answer(text=book_in_dict()[1], reply_markup=pagination_kb.create_pagination_kb(current_page=1))

@router.message(Command("continue"))
async def process_continue_message(message: Message) -> None:
    if message.from_user.id not in get_info():
        get_info()[message.from_user.id] = {"current_page" : 1}
        fill_database()
    await message.answer(text=book_in_dict()[get_info()[message.from_user.id]["current_page"]], reply_markup=pagination_kb.create_pagination_kb(current_page=get_info()[message.from_user.id]["current_page"]))
    
@router.message(Command("bookmarks"))
async def process_bookmarks_message(message: Message) -> None:
    await message.answer(text=LEXICON_RU["bookmarks"], reply_markup=bookmarks_kb.create_bookmarks_kb(get_info()[message.from_user.id]["bookmarks"], user_id=message.from_user.id))

@router.callback_query(F.data == "prev")
async def process_prev_callback(callback: CallbackQuery) -> None:
    if get_info()[callback.from_user.id]["current_page"] != 1:
        get_info()[callback.from_user.id]["current_page"] -= 1
        fill_database()
        await callback.message.edit_text(text=book_in_dict()[get_info()[callback.from_user.id]["current_page"]], reply_markup=pagination_kb.create_pagination_kb(current_page=get_info()[callback.from_user.id]["current_page"]))
    else:
        await callback.answer()

@router.callback_query(F.data == "next")
async def process_next_callback(callback: CallbackQuery) -> None:
    if get_info()[callback.from_user.id]["current_page"] != max(book_in_dict().keys()):
        get_info()[callback.from_user.id]["current_page"] += 1
        fill_database()
        await callback.message.edit_text(text=book_in_dict()[get_info()[callback.from_user.id]["current_page"]], reply_markup=pagination_kb.create_pagination_kb(current_page=get_info()[callback.from_user.id]["current_page"]))
    else:
        await callback.answer()

@router.callback_query(filters.IsDigitCallbackQuery())
async def process_save_callback(callback: CallbackQuery) -> None:
    if "bookmarks" not in get_info()[callback.from_user.id]:
        get_info()[callback.from_user.id]["bookmarks"] = []
    if f"{callback.data} - {book_in_dict()[int(callback.data)][:30]}..." not in get_info()[callback.from_user.id]["bookmarks"]:
        get_info()[callback.from_user.id]["bookmarks"].append(f"{callback.data} - {book_in_dict()[int(callback.data)][:30]}...")
    fill_database()
    await callback.answer()

@router.callback_query(filters.IsEditorCallbackQuery())
async def process_edit_bookmarks(callback: CallbackQuery) -> None:
    if len(get_info()[callback.from_user.id]["bookmarks"]) == 0:
        await callback.message.edit_text(text=LEXICON_RU["no_bookmarks"])
    else:
        await callback.message.edit_text(text=LEXICON_RU["edit"], reply_markup=bookmarks_kb.create_editor_kb(get_info()[callback.from_user.id]["bookmarks"], user_id=callback.from_user.id))

@router.callback_query(filters.IsEditCallbackQuery())
async def process_go_by_bookmarks(callback: CallbackQuery) -> None:
    await callback.message.answer(text=book_in_dict()[int(callback.data[:-4])], reply_markup=pagination_kb.create_pagination_kb(current_page=int(callback.data[:-4])))

@router.callback_query(filters.IsDeleterCallbackQuery())
async def process_delete_bookmark(callback: CallbackQuery) -> None:
    get_info()[callback.from_user.id]["bookmarks"] = [x for x in get_info()[callback.from_user.id]["bookmarks"] if not x.startswith(f"{callback.data[:-3]} -")]
    fill_database()
    if len(get_info()[callback.from_user.id]["bookmarks"]) == 0:
        await callback.message.edit_text(text=LEXICON_RU["no_bookmarks"])
    else:
        await callback.message.edit_text(text=LEXICON_RU["edit"], reply_markup=bookmarks_kb.create_editor_kb(get_info()[callback.from_user.id]["bookmarks"], user_id=callback.from_user.id))

@router.callback_query(filters.IsBookmarkCancel())
async def process_cancel_bookmark(callback: CallbackQuery) -> None:
    await callback.message.edit_text(text=LEXICON_RU["continue"])

@router.callback_query(filters.IsDeleterCancel())
async def process_cancel_deleter(callback: CallbackQuery) -> None:
    if len(get_info()[callback.from_user.id]["bookmarks"]) == 0:
        await callback.message.edit_text(text=LEXICON_RU["no_bookmarks"])
    else:
        await callback.message.edit_text(text=LEXICON_RU["bookmarks"], reply_markup=bookmarks_kb.create_bookmarks_kb(get_info()[callback.from_user.id]["bookmarks"], user_id=callback.from_user.id))
