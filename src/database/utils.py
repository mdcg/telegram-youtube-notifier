import os
import sqlite3
import sys
from contextlib import contextmanager

from src.database import logger
from src.settings import DATABASE_URL
import psycopg2


@contextmanager
def get_connection():
    conn = psycopg2.connect(DATABASE_URL)
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
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f"Failed to insert data into sqlite. {error}")

    return None


def save_user(chat_id):
    logger.info(
        f"Initializing process to save data related to users - Values: ({chat_id})"
    )
    sql = "INSERT INTO users (chat_id) VALUES (%s);"
    insert_data(sql, (chat_id,))
    return None


def save_channel(channel_id):
    logger.info(
        f"Initializing process to save data related to channels - Values: ({channel_id})"
    )
    sql = "INSERT INTO channels (channel_id) VALUES (%s);"
    insert_data(sql, (channel_id,))
    return None


def subscribe_user(channel_id, chat_id):
    relation_id = f"{channel_id}_{chat_id}"
    logger.info(
        f"Initializing process to save data related to notifications - Values: ({relation_id}, {channel_id}, {chat_id})"
    )
    sql = "INSERT INTO notifications (relation_id, channel_id, chat_id) VALUES (%s, %s, %s);"
    insert_data(sql, (relation_id, channel_id, chat_id))
    return None


def search_for_subscribed_users(channel_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT chat_id FROM notifications WHERE channel_id = %s;",
            (channel_id,),
        )
        users = cursor.fetchall()

    return [user[0] for user in users]
