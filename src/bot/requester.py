import requests
from src.settings import CALLBACK_URL
from src.bot import logger


def subscribe_in_pubsubhubbub(channel_id: str) -> int:
    """The subscription request to find out when a new video arrives on a
    specific channel is made from this function. Basically here the
    necessary data for this activity is informed for Pubsubhubbub

    Parameters
    ----------
    channel_id : str
        YouTube channel identifier.

    Returns
    -------
    int
        HTTP status code reported by pubsubhubbub in response.
    """
    logger.info("Sending subscribe request to Pubsubhubbub..")
    payload = {
        "hub.callback": CALLBACK_URL,
        "hub.topic": f"https://www.youtube.com/xml/feeds/videos.xml?channel_id={channel_id}",
        "hub.mode": "subscribe",
        "hub.lease_seconds": 60 * 60 * 24 * 5,
    }
    r = requests.post(
        "https://pubsubhubbub.appspot.com/subscribe", data=payload
    )
    logger.info(f"Callback URL: {CALLBACK_URL}")
    logger.info(
        f"Checking for possible message received from pubsubhubbub: {r.text}"
    )
    return r.status_code
