import os
import sqlite3
import sys

from src.database import logger


def delete_db():
    logger.info("Deleting an existing database..")
    if os.path.exists("youtube_notifications.db"):
        os.remove("youtube_notifications.db")
    return None


def init_db():
    conn = sqlite3.connect("youtube_notifications.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (chat_id VARCHAR(255) PRIMARY KEY);")
    cursor.execute(
        "CREATE TABLE channels (channel_id VARCHAR(255) PRIMARY KEY);"
    )
    cursor.execute(
        "CREATE TABLE notifications (relation_id VARCHAR(255) PRIMARY KEY, channel_id VARCHAR(255) NOT NULL, chat_id VARCHAR(255) NOT NULL);"
    )
    conn.close()
    return None


if __name__ == "__main__":
    logger.info("Initializing generate_db script.")
    delete_db()
    init_db()
    logger.info("Youtube Notifications DB successfully created.")
