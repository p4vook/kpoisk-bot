import pytest

from aiogram.filters import Command
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE

from kinopoisk_unofficial_api_client import Client

from kpoisk_bot.handlers import command_start_handler, search_handler

import httpx


@pytest.mark.asyncio
async def test_command_handler():
    requester = MockedBot(
        MessageHandler(command_start_handler, Command(commands=["start"]))
    )
    calls = await requester.query(MESSAGE.as_object(text="/start"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Hello, <b>FirstName LastName</b>!"


class MyMiddleware:
    def __init__(self, httpx_client):
        self.client = Client(base_url="https://example.com")
        self.client.set_async_httpx_client(httpx_client)

    async def __call__(self, handler, event, data):
        data["api_client"] = self.client
        return await handler(event, data)


JSON_RESPONSE = {
    "films": [
        {
            "countries": [],
            "filmId": 1,
            "nameRu": "ru",
            "nameEn": "en",
            "type": "FILM",
            "year": "2007",
            "description": "desc",
            "filmLength": "1",
            "genres": [{"genre": "комедия"}, {"genre": "хоррор"}],
            "posterUrl": "https://POST",
            "posterUrlPreview": "https://PREVIEW",
            "rating": "5.7",
            "rating_vote_count": 57,
        }
    ],
    "keyword": "тест",
    "pagesCount": 0,
    "searchFilmsCountResult": 7,
}


@pytest.mark.asyncio
async def test_search_handler(httpx_mock):
    httpx_mock.add_response(json=JSON_RESPONSE)
    async with httpx.AsyncClient(base_url="https://example.com") as client:
        requester = MockedBot(
            MessageHandler(search_handler, dp_middlewares=[MyMiddleware(client)])
        )
        calls = await requester.query(MESSAGE.as_object(text="тест"))
        answer_message = calls.send_message.fetchone()
        assert (
            answer_message.text
            == "Название: ru (фильм, 2007)\nЖанры: #комедия, #хоррор\nДлина: 1\n\nОписание: desc\n"
        )
