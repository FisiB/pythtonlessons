from database import get_connection

conn = get_connection()
cursor = conn.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    admin BOOLEAN DEFAULT 0
)
""")

# Players table
cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Player TEXT,
    Nation TEXT,
    Squad TEXT,
    Pos TEXT,
    Gls INTEGER,
    Ast INTEGER
)
""")

# Articles table
cursor.execute("""
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT,
    author TEXT
)
""")

# Favorite XI table
cursor.execute("""
CREATE TABLE IF NOT EXISTS favorite_xi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    player_list TEXT
)
""")

conn.commit()
conn.close()
print("Database initialized successfully")
