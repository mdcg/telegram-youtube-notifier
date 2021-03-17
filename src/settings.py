from decouple import config


TELEGRAM_TOKEN = config("TELEGRAM_TOKEN", "")
CALLBACK_URL = config("CALLBACK_URL", "")
