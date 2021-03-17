from src.settings import TELEGRAM_TOKEN
from telegram import Bot
from src.server import logger


bot = Bot(TELEGRAM_TOKEN)


def send_telegram_notification(chat_id, link, title, author):
    logger.info(f"Sending notification to {chat_id}")
    bot.send_message(
        chat_id=chat_id, text=f"New video from {author}!\n\n{link}"
    )
