from typing import Optional

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from src.database.utils import search_for_subscribed_users
from src.settings import TELEGRAM_TOKEN
from telegram import Bot

app = FastAPI()


class Notification(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


# https://pubsubhubbub.github.io/PubSubHubbub/pubsubhubbub-core-0.4.html#rfc.section.5
# https://github.com/youtube/api-samples/issues/177
# ToDo: Adicionar requests no src.bot.core para inscrever usuário
@app.get("/notification")
async def notify_users(notification: Notification):
    bot = Bot(TELEGRAM_TOKEN)
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
