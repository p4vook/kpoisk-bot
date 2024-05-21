import textwrap
from typing import Tuple

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           InlineQueryResult, InlineQueryResultArticle,
                           InputTextMessageContent, LinkPreviewOptions)
from aiogram.utils.formatting import (Bold, HashTag, Italic, Text, TextLink,
                                      as_line, as_list)
from kinopoisk_unofficial_api_client.models import (Film,
                                                    FilmSearchResponseFilms)

from .config import DESCRIPTION_LENGTH, KINOPOISK_ROOT


class FilmFormatter:
    film: FilmSearchResponseFilms | Film

    def __init__(self, film: FilmSearchResponseFilms | Film) -> None:
        self.film = film

    def get_id(self) -> int:
        return (
            self.film.kinopoisk_id if isinstance(self.film, Film) else self.film.film_id
        )

    def is_valid(self) -> bool:
        return bool(self.get_id())

    def has_poster(self) -> bool:
        if isinstance(self.film, Film):
            return self.film.cover_url is not None
        return bool(self.film.poster_url) and bool(self.film.poster_url_preview)

    def get_poster(self) -> str | None:
        if isinstance(self.film, Film):
            return self.film.cover_url
        return self.film.poster_url if self.film.poster_url else None

    def get_poster_preview(self) -> str | None:
        return self.film.poster_url_preview if self.film.poster_url_preview else None

    def get_title(self) -> str:
        return self.film.name_ru or "Без названия"

    def get_type(self) -> str:
        DESCRIPTION = {
            "FILM": "фильм",
            "MINI_SERIES": "мини-сериал",
            "TV_SERIES": "сериал",
            "TV_SHOW": "ТВ-шоу",
            "VIDEO": "видео",
        }
        return DESCRIPTION[str(self.film.type)]

    def get_description(self) -> str:
        return self.film.description or "Без описания"

    def get_url(self) -> str:
        return f"{KINOPOISK_ROOT}/film/{self.get_id()}/"

    def get_year(self) -> str | None:
        return (
            str(self.film.year)
            if self.film.year and isinstance(self.film, Film)
            else (self.film.year if self.film.year else None)
        )

    def get_rating(self) -> Tuple[str, int] | None:
        if isinstance(self.film, Film):
            return (
                (
                    str(self.film.rating_kinopoisk),
                    self.film.rating_kinopoisk_vote_count,
                )
                if self.film.rating_kinopoisk and self.film.rating_kinopoisk_vote_count
                else None
            )
        return (
            (self.film.rating, self.film.rating_vote_count)
            if self.film.rating
            and self.film.rating != "null"
            and self.film.rating_vote_count
            else None
        )

    def get_title_description(self) -> str:
        return self.get_type() + ((", " + self.get_year()) if self.get_year() else "")

    def inline_title(self) -> str:
        return f"{self.get_title()} ({self.get_title_description()})"

    def inline_description(self) -> str:
        res = ""
        if self.film.genres:
            res += ", ".join(map(lambda g: g.genre, self.film.genres))
        return res

    def as_inline_content(self) -> InputTextMessageContent:
        link_options = None
        content = Text(self.inline_title())
        if self.has_poster():
            link_options = LinkPreviewOptions(is_disabled=False, show_above_text=True)
            content = TextLink(self.inline_title(), url=self.get_poster())
        return InputTextMessageContent(
            link_preview_options=link_options,
            **content.as_kwargs(text_key="message_text"),
        )

    def create_inline_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Посмотреть на КиноПоиске",
                        url=self.get_url(),
                    )
                ]
            ]
        )

    def as_inline(self) -> InlineQueryResult:
        return InlineQueryResultArticle(
            id=str(self.get_id()),
            title=self.inline_title(),
            description=self.inline_description(),
            thumbnail_url=self.get_poster_preview(),
            input_message_content=self.as_inline_content(),
            reply_markup=self.create_inline_markup(),
        )

    def title_component(self) -> Text:
        return as_line(
            Bold("Название:"),
            TextLink(self.get_title(), url=self.get_url()),
            Text(f"({self.get_title_description()})"),
            sep=" ",
        )

    def genres_component(self) -> Text | None:
        if self.film.genres:
            return as_line(
                Bold("Жанры:"),
                as_line(
                    *[HashTag(f"#{g.genre}") for g in self.film.genres],
                    end="",
                    sep=", ",
                ),
                sep=" ",
            )
        return None

    def rating_component(self) -> Text | None:
        rating_pair = self.get_rating()
        if rating_pair:
            rating, vote_count = rating_pair
            return as_line(
                Bold("Рейтинг:"),
                rating,
                Italic(f"({vote_count} оценок)"),
                sep=" ",
            )
        return None

    def length_component(self) -> Text | None:
        if self.film.film_length:
            return as_line(Bold("Длина:"), Text(self.film.film_length), sep=" ")
        return None

    def description_component(self) -> Text:
        return as_line(
            Bold("Описание:"),
            Text(
                textwrap.shorten(
                    self.get_description(),
                    DESCRIPTION_LENGTH,
                    placeholder="...",
                )
            ),
            sep=" ",
        )

    def text_message_content(self) -> Text:
        components = [self.title_component()]
        if genres_component := self.genres_component():
            components.append(genres_component)
        if rating_component := self.rating_component():
            components.append(rating_component)
        if length_component := self.length_component():
            components.append(length_component)
        components.append(Text("\n"))
        components.append(self.description_component())

        return as_list(*components, sep="")

    def as_text_message(self) -> InputTextMessageContent:
        link_options = None
        if self.has_poster():
            link_options = LinkPreviewOptions(
                is_disabled=False, url=self.get_poster(), show_above_text=True
            )

        content = self.text_message_content()
        return InputTextMessageContent(
            link_preview_options=link_options,
            **content.as_kwargs(text_key="message_text"),
        )

    def create_result_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Посмотреть на КиноПоиске",
                        url=self.get_url(),
                    )
                ]
            ]
        )
