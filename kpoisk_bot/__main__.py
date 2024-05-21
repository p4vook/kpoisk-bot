import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .config import TELEGRAM_TOKEN
from .handlers import router
from .session import ApiMiddleware


async def main() -> None:
    bot = Bot(
        token=TELEGRAM_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    session_middleware = ApiMiddleware()
    await session_middleware.init()
    router.message.middleware(session_middleware)
    router.inline_query.middleware(session_middleware)
    router.chosen_inline_result.middleware(session_middleware)

    dp = Dispatcher()
    dp.include_router(router)
    dp.shutdown()(session_middleware.on_shutdown)

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
