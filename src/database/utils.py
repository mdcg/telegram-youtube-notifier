import os
import sqlite3
import sys
from contextlib import contextmanager

from src.database import logger


@contextmanager
def get_connection():
    conn = sqlite3.connect("youtube_notifications.db")
    try:
        yield conn
    finally:
        conn.close()


def insert_data(sql, data):
    with get_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            logger.info("Data saved successfully.")
            cursor.close()
        except sqlite3.Error as error:
            logger.error(f"Failed to insert data into sqlite. {error}")
        finally:
            if conn:
                conn.close()
                logger.info("The SQLite connection is closed.")

    return None


def save_user(chat_id):
    logger.info(
        f"Initializing process to save data related to users - Values: ({chat_id})"
    )
    sql = "INSERT INTO users (chat_id) VALUES (?);"
    insert_data(sql, (chat_id,))
    return None


def save_channel(channel_id):
    logger.info(
        f"Initializing process to save data related to channels - Values: ({channel_id})"
    )
    sql = "INSERT INTO channels (channel_id) VALUES (?);"
    insert_data(sql, (channel_id,))
    return None


def subscribe_user(channel_id, chat_id):
    relation_id = f"{channel_id}_{chat_id}"
    logger.info(
        f"Initializing process to save data related to notifications - Values: ({relation_id}, {channel_id}, {chat_id})"
    )
    sql = "INSERT INTO notifications (relation_id, channel_id, chat_id) VALUES (?, ?, ?);"
    insert_data(sql, (relation_id, channel_id, chat_id))
    return None
