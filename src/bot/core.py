import sys

from src.bot import logger
from src.bot.messages import (
    AVAILABLE_COMMANDS_MESSAGE,
    GREETINGS_MESSAGE,
    NON_INFORMED_CHANNEL_ID_MESSAGE,
    SUBSCRIPTION_ERROR_MESSAGE,
    SUBSCRIPTION_MESSAGE,
    UNKNOWN_MESSAGE,
)
from src.bot.requester import subscribe_in_pubsubhubbub
from src.database.utils import save_channel, save_user, subscribe_user
from src.settings import TELEGRAM_TOKEN
from telegram.ext import (
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
    CallbackContext,
)
from telegram import Update


def start_command(update: Update, context: CallbackContext):
    """As soon as the bot is started, the first command that by default the
    user sends to it is '/start'. Here we define what will be answered,
    which in this case, is a customized message with the name of the user
    in question informing how he can interact with the bot.

    Parameters
    ----------
    update : Update
        This object represents an incoming update.
    context : CallbackContext
        This is a context object passed to the callback called by
        telegram.ext.Handler.
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=GREETINGS_MESSAGE.format(update.effective_chat.username),
    )
    return None


def help_command(update: Update, context: CallbackContext) -> None:
    """To assist the user in teaching how he will use the bot, we have
    specified this function that will give all the necessary
    instructions to him.

    Parameters
    ----------
    update : Update
        This object represents an incoming update.
    context : CallbackContext
        This is a context object passed to the callback called by
        telegram.ext.Handler.
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=AVAILABLE_COMMANDS_MESSAGE
    )
    return None


def unknown_command(update: Update, context: CallbackContext) -> None:
    """Some users can write commands that are not handled by the bot. In order
    not to make him anxious without knowing if something went right or not,
    any command that is not mapped by the service will be answered with a
    redirect to him using the command '/help'

    Parameters
    ----------
    update : Update
        This object represents an incoming update.
    context : CallbackContext
        This is a context object passed to the callback called by
        telegram.ext.Handler.
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=UNKNOWN_MESSAGE
    )
    return None


def subscribe_command(update: Update, context: CallbackContext) -> None:
    """This function is our "flagship". Basically this is where the user will
    be able to subscribe to a channel to receive notifications for new videos.

    Parameters
    ----------
    update : Update
        This object represents an incoming update.
    context : CallbackContext
        This is a context object passed to the callback called by
        telegram.ext.Handler.
    """
    try:
        channel_id = context.args[0]
    except IndexError:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=NON_INFORMED_CHANNEL_ID_MESSAGE,
        )
        return None

    logger.info("Channel subscription requested. Initializing processing.")

    chat_id = update.effective_chat.id
    save_user(chat_id)
    status = subscribe_in_pubsubhubbub(channel_id)

    if status == 202:
        logger.info("Request sent successfully.")
        save_channel(channel_id)
        subscribe_user(channel_id, chat_id)
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=SUBSCRIPTION_MESSAGE
        )
    else:
        logger.warning(
            f"There was a problem sending your subscribe request. Status Code received: {status}"
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=SUBSCRIPTION_ERROR_MESSAGE
        )

    return None


def main() -> None:
    """This is where the bot will actually start and handle requests with
    Telegram users.
    """
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
