import os
import sqlite3
import sys
from contextlib import contextmanager

from src.database import logger
from src.settings import DATABASE_URL
import psycopg2


@contextmanager
def get_connection():
    """Context managers allow you to allocate and release resources precisely
    when you want to. The most widely used example of context managers is the
    with statement. This one in particular generates a connection to
    PostgreSQL.

    Yields
    -------
    psycopg2.connection
        Handles the connection to a PostgreSQL database instance.
        It encapsulates a database session.
    """
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()


def insert_data(sql: str, data: str) -> None:
    """From a PostgreSQL clause related to data insertion, and also, from a
    data tuple referring to what you want to save, insert the data into the
    database.

    Parameters
    ----------
    sql : str
        Clause that should be used to insert some entry in the database.
    data : tuple
        Data that must be inserted in the bank and that must be related to
        the entries established by the variable "sql".
    """
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


def save_user(chat_id: str) -> None:
    """Insert the "chat_id" (user identifier in the Telegram) in the database.

    Parameters
    ----------
    chat_id : str
        User identifier in the Telegram.
    """
    logger.info(
        f"Initializing process to save data related to users - Values: ({chat_id})"
    )
    sql = "INSERT INTO users (chat_id) VALUES (%s);"
    insert_data(sql, (chat_id,))
    return None


def save_channel(channel_id: str) -> None:
    """Insert the "channel_id" (YouTube channel identifier) ​​in the database.

    Parameters
    ----------
    channel_id : str
        YouTube channel identifier.
    """
    logger.info(
        f"Initializing process to save data related to channels - Values: ({channel_id})"
    )
    sql = "INSERT INTO channels (channel_id) VALUES (%s);"
    insert_data(sql, (channel_id,))
    return None


def subscribe_user(channel_id: str, chat_id: str) -> None:
    """Creates a relationship between chat_id (user identifier in the Telegram)
    and channel_id (YouTube channel identifier) ​​in the database.

    Parameters
    ----------
    channel_id : str
        User identifier in the Telegram.
    chat_id : str
        YouTube channel identifier.
    """
    relation_id = f"{channel_id}_{chat_id}"
    logger.info(
        f"Initializing process to save data related to notifications - Values: ({relation_id}, {channel_id}, {chat_id})"
    )
    sql = "INSERT INTO notifications (relation_id, channel_id, chat_id) VALUES (%s, %s, %s);"
    insert_data(sql, (relation_id, channel_id, chat_id))
    return None


def search_for_subscribed_users(channel_id: str) -> list:
    """Searches for all users who have subscribed to a specific channel.

    Parameters
    ----------
    channel_id : str
        YouTube channel identifier.

    Returns
    -------
    list
        List containing all users who have subscribed to a specific channel.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT chat_id FROM notifications WHERE channel_id = %s;",
            (channel_id,),
        )
        users = cursor.fetchall()

    # Regardless of the amount of data selected, the result is always a tuple.
    # In this way, as we only want "chat_id", we access the first index.
    return [user[0] for user in users]
