# DATABASE CONNECTOR  - db_utils.py
# ------------------------------------------------------------
# Handles all MySQL database connections and query execution
# for the EVCS Threat Intelligence API. Uses exception handling
# to gracefully manage database errors.
# ------------------------------------------------------------

import mysql.connector
from mysql.connector import Error
import config


def get_connection():
    """
    Creates and returns a connection to the MySQL database
    using credentials defined in config.py.
    Raises an exception if the connection fails.
    """
    try:
        connection = mysql.connector.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        return connection

    except Error as e:
        raise ConnectionError(f"Failed to connect to database: {e}")


def execute_query(query, params=None):
    """
    Executes a write query (INSERT, UPDATE, DELETE) against the database.
    Returns the last inserted row ID on success.
    Raises an exception if the query fails.

    Args:
        query  (str):  The SQL query string with %s placeholders.
        params (tuple): Optional tuple of values to substitute.
    """
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        connection.commit()
        return cursor.lastrowid

    except Error as e:
        raise RuntimeError(f"Database query failed: {e}")

    finally:
        # Always close cursor and connection to avoid resource leaks
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def fetch_query(query, params=None):
    """
    Executes a read query (SELECT) and returns all matching rows
    as a list of dictionaries keyed by column name.

    Args:
        query  (str):  The SQL SELECT query string with %s placeholders.
        params (tuple): Optional tuple of values to substitute.
    """
    connection = None
    cursor = None
    try:
        connection = get_connection()
        # dictionary=True makes each row a dict instead of a plain tuple
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        return results

    except Error as e:
        raise RuntimeError(f"Database fetch failed: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()