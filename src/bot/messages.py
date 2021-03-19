"""
To make it a little easier to manage the messages sent by Bot, we have allocated
them all here.
"""

GREETINGS_MESSAGE = (
    "Greetings, honorable {}! Use the '/help' command for more information!"
)
AVAILABLE_COMMANDS_MESSAGE = "This bot is intended to notify you as soon as a new video from a channel that you are subscribed to is available. For that, you only need to inform the channel ID that you want to receive notifications and the rest is up to us! To do this, use the command '/subscribe <CHANNEL_ID>'"
UNKNOWN_MESSAGE = "Sorry, we were unable to understand your request. Use the '/help' command for more usage information."
SUBSCRIPTION_MESSAGE = "You are now subscribed to the informed channel. As soon as new videos are added, you will be informed."
NON_INFORMED_CHANNEL_ID_MESSAGE = "You need to enter the desired channel id. For example, the URL ID 'https://www.youtube.com/channel/UC3VHfy8e1jbDnT5TG2pjP1w' is 'UC3VHfy8e1jbDnT5TG2pjP1w'."
SUBSCRIPTION_ERROR_MESSAGE = "It was not possible to subscribe to the indicated channel. Are you sure everything is specified correctly?"
