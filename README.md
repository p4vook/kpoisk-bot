# Telegram bot to search for movies in Kinopoisk

(Heavily inspired by @imdbot)

Functionality: 

- Inline mode:

  Type "@kpoiskbot search string" anywhere in Telegram, and see
  matching candidates. 

  When you see the one you looked for, click on it, and the bot will 
  format the movie information as a Telegram message.

- User settings:

  User can directly message the bot in Telegram and issue a /settings
  command. In response bot sends a message with all the settings that 
  can be changed formatted as buttons.

How it is implemented:

* It uses API from https://kinopoiskapiunofficial.tech/
* It uses a Postgres database to store user settings and cache API results
* It uses telethon to communicate with Telegram
* Everything is orchestrated using Docker-Compose

Libraries:

* `aiogram` (communicating with Telegram)
* `httpx` (communicating with API)
* `beanie` (ORM)
* `pydantic` (model validation)
