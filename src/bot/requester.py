import requests
from src.settings import CALLBACK_URL


def subscribe_in_pubsubhubbub(channel_id):
    payload = {
        "hub.callback": CALLBACK_URL,
        "hub.topic": f"https://www.youtube.com/xml/feeds/videos.xml?channel_id={channel_id}",
        "hub.mode": "subscribe",
    }
    r = requests.post('https://pubsubhubbub.appspot.com/subscribe', data=payload)
    return r.status_code
