from src.settings import TELEGRAM_TOKEN
from telegram import Bot
from src.server import logger


bot = Bot(TELEGRAM_TOKEN)


def send_telegram_notification(
    chat_id: str, link: str, title: str, author: str
) -> None:
    """Sends a notification with the data of a new video from a YouTube channel
    to a specific user.

    Parameters
    ----------
    chat_id : str
        User identifier in the Telegram.
    link : str
        URL for the new video.
    title : str
        Video title.
    author : str
        Name of the channel that uploaded the new video.
    """
    logger.info(f"Sending notification to {chat_id}")
    bot.send_message(
        chat_id=chat_id, text=f"New video from {author}!\n\n{link}"
    )
    return None
