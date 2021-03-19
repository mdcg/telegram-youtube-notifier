import xml.etree.ElementTree as ET
from typing import Optional

import uvicorn
from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel
from src.database.utils import search_for_subscribed_users
from src.server.bot import send_telegram_notification
from src.server import logger
from src.settings import PORT

app = FastAPI()


@app.get("/feed")
async def feed_challenge(request: Request, response: Response):
    challenge = request.query_params.get("hub.challenge")
    logger.info(f"RECEIVED CHALLENGE: {challenge}")
    if challenge:
        return Response(
            challenge, status_code=status.HTTP_200_OK, media_type="text/plain"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/feed", status_code=200)
async def notify_users(request: Request, response: Response):
    atom = "{http://www.w3.org/2005/Atom}"
    yt = "{http://www.youtube.com/xml/schemas/2015}"

    pubsubhubbub_request_body = await request.body()
    root = ET.fromstring(pubsubhubbub_request_body)

    try:
        entry = root.find(f"{atom}entry")
        channel_id = entry.find(f"{yt}channelId").text

        author_tag = entry.find(f"{atom}author")
        author = author_tag.find(f"{atom}name").text
        link = entry.find(f"{atom}link").get("href")
        title = entry.find(f"{atom}title").text
    except AttributeError as err:
        logger.info(f"There was an error while receiving the XML: {err}")
        logger.info(f"XML received: {pubsubhubbub_request_body}")
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST, media_type="text/plain"
        )

    channels_id = search_for_subscribed_users(channel_id)
    for ch_id in channels_id:
        send_telegram_notification(ch_id, link, title, author)

    context = {
        "channel_id": channel_id,
        "link": link,
        "title": title,
        "author": author,
    }
    return Response(
        context, status_code=status.HTTP_200_OK, media_type="application/json"
    )
