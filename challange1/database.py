import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    # Make sure the DATABASE_URL is correct for SQLite or your actual database
    connection = sqlite3.connect(DATABASE_URL)
    cursor=connection.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    director TEXT NOT NULL
);"""
    )
    connection.commit()
    connection.close()

    connection.row_factory = sqlite3.Row  # Allows for dict-like access to rows
    return connection

