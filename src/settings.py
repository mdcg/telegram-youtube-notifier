from decouple import config


TELEGRAM_TOKEN = config("TELEGRAM_TOKEN", "")
CALLBACK_URL = config("CALLBACK_URL", "")
PORT = config("PORT", 5000, cast=int)
