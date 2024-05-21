import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from kinopoisk_unofficial_api_client import AuthenticatedClient

from .config import API_TOKEN, API_URL


class ApiMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.client = AuthenticatedClient(base_url=API_URL, token=API_TOKEN)

    async def init(self) -> None:
        await self.client.__aenter__()
        logging.info(f"Established connection to API at {API_URL}")

    async def on_shutdown(self) -> None:
        await self.client.__aexit__()
        logging.info("Shut down API connection")

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["api_client"] = self.client
        return await handler(event, data)
