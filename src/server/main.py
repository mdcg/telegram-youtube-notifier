import xml.etree.ElementTree as ET
from typing import Optional

import uvicorn
from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel
from src.database.utils import search_for_subscribed_users
from src.server.bot import send_telegram_notification
from src.server import logger

app = FastAPI()


# https://pubsubhubbub.github.io/PubSubHubbub/pubsubhubbub-core-0.4.html#rfc.section.5
# https://pubsubhubbub.github.io/PubSubHubbub/pubsubhubbub-core-0.4.html#verifysub
@app.get("/feed")
async def feed_challenge(request: Request, response: Response):
    challenge = request.query_params.get("hub.challenge")
    logger.info(f"RECEIVED CHALLENGE: {challenge}")
    if challenge:
        return Response(challenge, status_code=status.HTTP_200_OK, media_type="text/plain")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/feed", status_code=200)
async def notify_users(request: Request, response: Response):
    atom = "{http://www.w3.org/2005/Atom}"
    yt = "{http://www.youtube.com/xml/schemas/2015}"

    pubsubhubbub_request_body = await request.body()
    root = ET.fromstring(pubsubhubbub_request_body)

    entry = root.find(f"{atom}entry")
    channel_id = entry.find(f"{yt}channelId").text
    
    author_tag = entry.find(f"{atom}author")
    author = author_tag.find(f"{atom}name").text
    link = entry.find(f"{atom}link").get("href")
    title = entry.find(f"{atom}title").text

    channels_id = search_for_subscribed_users(channel_id)
    for ch_id in channels_id:
        send_telegram_notification(ch_id, link, title, author)

    return {
        "channel_id": channel_id,
        "link": link,
        "title": title,
        "author": author,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
