from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU

router = Router()

@router.message()
async def process_incorrect_message(message: Message) -> None:
    await message.answer(text=LEXICON_RU["undefined"])