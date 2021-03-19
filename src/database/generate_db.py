import os
import psycopg2
import sys

from src.database.utils import get_connection
from src.database import logger
import psycopg2


def init_db() -> None:
    """We need to ensure that the database works with a specific rule. Thus,
    this function is called whenever a new version of the system goes into
    production.
    """
    with get_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS users (chat_id varchar(255) NOT NULL, PRIMARY KEY (chat_id));"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS channels (channel_id varchar(255) NOT NULL, PRIMARY KEY (channel_id));"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS notifications (relation_id varchar(255) NOT NULL, channel_id varchar(255) NOT NULL, chat_id varchar(255) NOT NULL, PRIMARY KEY (relation_id));"
            )
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f"Failed to insert data into sqlite. {error}")

    return None


if __name__ == "__main__":
    logger.info("Initializing generate_db script.")
    init_db()
    logger.info("Youtube Notifications DB successfully created.")
