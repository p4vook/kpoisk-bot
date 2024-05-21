from os import environ

TELEGRAM_TOKEN: str = environ["KPOISK_TELEGRAM_TOKEN"]
API_TOKEN: str = environ["KPOISK_API_TOKEN"]
API_URL: str = environ.get(
    "KPOISK_API_URL", default="https://kinopoiskapiunofficial.tech"
)
KINOPOISK_ROOT: str = environ.get(
    "KPOISK_KINOPOISK_ROOT", default="https://kinopoisk.ru"
)
DESCRIPTION_LENGTH: int = int(environ.get("KPOISK_DESCRIPTION_LENGTH", default="500"))
TOP_RESULTS_COUNT: int = int(environ.get("KPOISK_TOP_RESULTS_COUNT", default="5"))
