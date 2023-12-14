import asyncio
from aiogram import Bot, Dispatcher
from config.config import load_config, Config
from handlers import other_handlers, user_handlers

async def main() -> None:
    config: Config = load_config(".env")
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    
    dp = Dispatcher()
    dp.include_routers(user_handlers.router, other_handlers.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())