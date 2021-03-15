import sys

from decouple import config
from src.bot import logger
from src.bot.messages import (
    AVAILABLE_COMMANDS_MESSAGE,
    GREETINGS_MESSAGE,
    UNKNOWN_MESSAGE,
    SUBSCRIPTION_MESSAGE,
    NON_INFORMED_CHANNEL_ID_MESSAGE,
)
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from src.database.utils import save_channel, save_user, subscribe_user


TELEGRAM_TOKEN = config("TELEGRAM_TOKEN", "")


def start_command(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=GREETINGS_MESSAGE.format(update.effective_chat.username),
    )
    return None


def help_command(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=AVAILABLE_COMMANDS_MESSAGE
    )
    return None


def unknown_command(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=UNKNOWN_MESSAGE
    )
    return None


def subscribe_command(update, context):
    try:
        channel_id = context.args[0]
        chat_id = update.effective_chat.id

        save_user(chat_id)
        save_channel(channel_id)
        subscribe_user(channel_id, chat_id)

        context.bot.send_message(
            chat_id=update.effective_chat.id, text=SUBSCRIPTION_MESSAGE
        )
    except IndexError:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=NON_INFORMED_CHANNEL_ID_MESSAGE,
        )

    return None


def main():
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("subscribe", subscribe_command))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown_command))
    updater.start_polling()
    updater.idle()
    return None


if __name__ == "__main__":
    logger.info("Initializing bot...")
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Stopping bot...")
        sys.exit(0)
