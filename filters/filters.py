from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery

class IsDigitCallbackQuery(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.isdigit()

class IsDeleterCallbackQuery(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith("del") and callback.data[:-3].isdigit()
    
class IsEditCallbackQuery(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith("edit") and callback.data[:-4].isdigit()

class IsEditorCallbackQuery(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == "editor"

class IsBookmarkCancel(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == "cancel_in_bookmark"

class IsDeleterCancel(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == "cancel_in_deleter"