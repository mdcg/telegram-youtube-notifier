import xml.etree.ElementTree as ET
from typing import Optional

import uvicorn
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.database.utils import search_for_subscribed_users
from src.server.bot import send_telegram_notification
from src.server import logger
from src.settings import PORT

app = FastAPI()


@app.get("/feed")
async def feed_challenge(request: Request, response: Response) -> Response:
    """As soon as there is a 'subscription' request, Pubsubhubbub sends us a
    request with some "confirmation" subscription data. Basically, this
    function provides all the necessary treatment for the subscription
    to be successful.

    Parameters
    ----------
    request : Request
        FastAPI has several useful abstractions for handling request data.
        However, the way Pubsubhubbub sends us the data is a little different:
        They send us via query parameters in the URL. In this way, this object
        helps us to deal with this type of situation.
    response : Response
        We also need to send an empty response body to Pubsubhubbub. Due to the
        abstractions of FastAPI, the way we send a more "customized" response
        is using the Response object.

    Returns
    -------
    Response
        Response according to what is specified by Pubsubhubbub in case of
        success or failure.
    """
    challenge = request.query_params.get("hub.challenge")
    logger.info(f"RECEIVED CHALLENGE: {challenge}")
    if challenge:
        return Response(
            challenge, status_code=status.HTTP_200_OK, media_type="text/plain"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/feed", status_code=200)
async def notify_users(request: Request, response: Response) -> Response:
    """Pubsubhubbub sends us notifications whenever new videos are available.
    This route receives the data sent by it (which in this case is an XML) and
    does all the processing of extracting relevant content to then notify
    users subscribed to the channel by Telegram.

    Parameters
    ----------
    request : Request
        FastAPI has several useful abstractions for handling request data.
        However, the way Pubsubhubbub sends us the data is a little different:
        To notify that new videos have arrived, he sends us an XML containing
        all the information of the video, channel, etc.
    response : Response
        We also need to send an empty response body to Pubsubhubbub. Due to the
        abstractions of FastAPI, the way we send a more "customized" response
        is using the Response object.

    Returns
    -------
    Response
        Response according to what is specified by Pubsubhubbub in case of
        success or failure.
    """
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
        # Some errors can happen here since Pubsubhubbub does not necessarily
        # send us notifications for new videos only. If the YouTube channel
        # makes any changes to a video, or even deletes it, we will be
        # notified. Anyway, these other types of notifications are not of
        # interest to us at the moment.
        logger.info(f"There was an error while receiving the XML: {err}")
        logger.info(f"XML received: {pubsubhubbub_request_body}")
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST, media_type="text/plain"
        )

    channels_id = search_for_subscribed_users(channel_id)
    for ch_id in channels_id:
        send_telegram_notification(ch_id, link, title, author)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "channel_id": channel_id,
            "link": link,
            "title": title,
            "author": author,
        },
    )
