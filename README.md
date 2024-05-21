# Telegram bot to search for movies in Kinopoisk

(Heavily inspired by @imdbot)

Functionality: 

- Inline mode:

  Type "@kpoiskbot search string" anywhere in Telegram, and see
  matching candidates. 

  When you see the one you looked for, click on it, and the bot will 
  format the movie information as a Telegram message.

- User mode:

  User can directly message the bot in Telegram. The bot will search films
  by that message text and send them one-by-one.

How it is implemented:

* It uses API from https://kinopoiskapiunofficial.tech/, with an auto-generated client
* It uses `aiogram` to communicate with Telegram

Libraries:

* `aiogram` (communicating with Telegram)
* `httpx` (communicating with API)
* `pydantic` (model validation)
