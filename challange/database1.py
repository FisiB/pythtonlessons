import sqlite3

def create_connection():
    connection = sqlite3.connect("books.db")
    connection.row_factory = sqlite3.Row
    return connection
