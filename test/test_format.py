from kpoisk_bot.format import FilmFormatter
from kinopoisk_unofficial_api_client.models import FilmSearchResponseFilms, Genre

from aiogram.types import (
    InputTextMessageContent,
    LinkPreviewOptions,
    MessageEntity,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
)

import pytest

SIMPLE_FILM = FilmSearchResponseFilms(
    film_id=1,
    name_ru="ru",
    name_en="en",
    type="FILM",
    year="2007",
    description="desc",
    film_length="1",
    genres=[Genre("комедия"), Genre("хоррор")],
    poster_url="https://POST",
    poster_url_preview="https://PREVIEW",
    rating="5.7",
    rating_vote_count=57,
)


@pytest.fixture
def search_formatter() -> FilmFormatter:
    return FilmFormatter(SIMPLE_FILM)


def test_id(search_formatter):
    assert search_formatter.get_id() == 1


def test_valid(search_formatter):
    assert search_formatter.is_valid()


def test_poster(search_formatter):
    assert search_formatter.has_poster()
    assert search_formatter.get_poster() == "https://POST"
    assert search_formatter.get_poster_preview() == "https://PREVIEW"


def test_title(search_formatter):
    assert search_formatter.get_title() == "ru"


def test_year(search_formatter):
    assert search_formatter.get_year() == "2007"


def test_rating(search_formatter):
    assert search_formatter.get_rating() == ("5.7", 57)


def test_title_description(search_formatter):
    assert search_formatter.get_title_description()


def test_inline_title(search_formatter):
    assert search_formatter.inline_title() == "ru (фильм, 2007)"


def test_inline_description(search_formatter):
    assert search_formatter.inline_description() == "комедия, хоррор"


def test_inline_content(search_formatter):
    print(search_formatter.as_inline_content())
    assert search_formatter.as_inline_content() == InputTextMessageContent(
        link_preview_options=LinkPreviewOptions(
            is_disabled=False, show_above_text=True
        ),
        message_text="ru (фильм, 2007)",
        parse_mode=None,
        entities=[
            MessageEntity(type="text_link", offset=0, length=16, url="https://POST")
        ],
    )


def test_inline_markup(search_formatter):
    assert search_formatter.create_inline_markup() == InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Посмотреть на КиноПоиске", url="https://kinopoisk.ru/film/1/"
                )
            ]
        ]
    )


def test_as_inline(search_formatter):
    assert search_formatter.as_inline() == InlineQueryResultArticle(
        id="1",
        title="ru (фильм, 2007)",
        description="комедия, хоррор",
        thumbnail_url="https://PREVIEW",
        input_message_content=search_formatter.as_inline_content(),
        reply_markup=search_formatter.create_inline_markup(),
    )


def test_as_text_message(search_formatter):
    assert search_formatter.as_text_message() == InputTextMessageContent(
        message_text="""Название: ru (фильм, 2007)
Жанры: #комедия, #хоррор
Рейтинг: 5.7 (57 оценок)
Длина: 1

Описание: desc
""",
        parse_mode=None,
        entities=[
            MessageEntity(type="bold", offset=0, length=9),
            MessageEntity(
                type="text_link",
                offset=10,
                length=2,
                url="https://kinopoisk.ru/film/1/",
            ),
            MessageEntity(type="bold", offset=27, length=6),
            MessageEntity(type="hashtag", offset=34, length=8),
            MessageEntity(type="hashtag", offset=44, length=7),
            MessageEntity(type="bold", offset=52, length=8),
            MessageEntity(type="italic", offset=65, length=11),
            MessageEntity(type="bold", offset=77, length=6),
            MessageEntity(type="bold", offset=87, length=9),
        ],
        link_preview_options=LinkPreviewOptions(
            is_disabled=False, url="https://POST", show_above_text=True
        ),
    )


def test_result_markup(search_formatter):
    assert search_formatter.create_result_markup() == InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Посмотреть на КиноПоиске", url="https://kinopoisk.ru/film/1/"
                )
            ]
        ]
    )
