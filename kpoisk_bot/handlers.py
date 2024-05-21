import logging
from typing import Any

from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.types import (
    ChosenInlineResult,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message,
)
from httpx import HTTPError
from kinopoisk_unofficial_api_client import Client
from kinopoisk_unofficial_api_client.api.films import (
    get_api_v2_1_films_search_by_keyword,
    get_api_v2_2_films_id,
)

from .config import TOP_RESULTS_COUNT
from .format import FilmFormatter


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@router.message()
async def search_handler(message: Message, api_client: Client) -> Any:
    if message.text is None:
        return
    try:
        results = await get_api_v2_1_films_search_by_keyword.asyncio(
            client=api_client, keyword=message.text, page=1
        )
        for content in map(
            lambda film: FilmFormatter(film).as_text_message(),
            results.films[:TOP_RESULTS_COUNT],
        ):
            await message.reply(
                content.message_text,
                link_preview_options=content.link_preview_options,
                entities=content.entities,
                parse_mode=content.parse_mode,
            )
    except HTTPError as e:
        # But not all the types is supported to be copied so need to handle it
        logging.error(e)


@router.inline_query()
async def inline_handler(query: InlineQuery, api_client: Client) -> Any:
    if not query.query:
        return await query.answer(
            [
                InlineQueryResultArticle(
                    id="EMPTY",
                    title="Наберите название фильма, чтобы найти его в КиноПоиске",
                    input_message_content=InputTextMessageContent(
                        message_text="Этот бот поможет вам найти фильм в КиноПоиске"
                    ),
                )
            ]
        )

    try:
        api_result = await get_api_v2_1_films_search_by_keyword.asyncio(
            client=api_client, keyword=query.query, page=1
        )
        results = [
            FilmFormatter(film).as_inline()
            for film in api_result.films[:TOP_RESULTS_COUNT]
        ]
        return await query.answer(results)
    except (HTTPError, TypeError) as e:
        logging.error(e)
        return await query.answer(
            [
                InlineQueryResultArticle(
                    id="ERROR",
                    title="Упс, что-то пошло не так",
                    input_message_content=InputTextMessageContent(
                        message_text="Что-то пошло не так :("
                    ),
                )
            ]
        )


@router.chosen_inline_result()
async def chosen_inline_handler(result: ChosenInlineResult, api_client: Client) -> Any:
    if result.result_id == "ERROR" or result.result_id == "EMPTY":
        return

    film = await get_api_v2_2_films_id.asyncio(
        id=int(result.result_id), client=api_client
    )
    formatter = FilmFormatter(film)
    as_message = formatter.as_text_message()
    await result.bot.edit_message_text(
        inline_message_id=result.inline_message_id,
        text=as_message.message_text,
        parse_mode=as_message.parse_mode,
        entities=as_message.entities,
        link_preview_options=as_message.link_preview_options,
    )
    await result.bot.edit_message_reply_markup(
        inline_message_id=result.inline_message_id,
        reply_markup=formatter.create_result_markup(),
    )
