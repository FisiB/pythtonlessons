import os
import sqlite3
from typing import Optional
from datetime import datetime
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
DB_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.environ.get("DATABASE_PATH", os.path.join(DB_DIR, "finance.db"))

def _ensure_dir():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_db():
    _ensure_dir()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            type TEXT NOT NULL,
            category TEXT,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

# --- Users (PLAIN TEXT for course project) ---
def register_user(username: str, password: str) -> bool:
    if not username or not password:
        return False
    _ensure_dir()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        # Storing plain text password (Not for production)
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_password(username: str) -> Optional[str]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def authenticate_user(username: str, password: str) -> bool:
    stored = get_password(username)
    if not stored:
        return False
    # Direct comparison (Plain text)
    return password == stored

# --- Transactions ---
def add_transaction(username: str, t_type: str, category: str, amount: float, date: Optional[str] = None) -> int:
    _ensure_dir()
    if date is None:
        date = datetime.today().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO transactions (username, type, category, amount, date) VALUES (?, ?, ?, ?, ?)",
        (username, t_type, category, float(amount), date),
    )
    tx_id = c.lastrowid
    conn.commit()
    conn.close()
    return tx_id

def get_transactions(username: str) -> pd.DataFrame:
    _ensure_dir()
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(
            "SELECT * FROM transactions WHERE username = ? ORDER BY date DESC, id DESC", conn, params=(username,)
        )
    finally:
        conn.close()
    return df


def update_transaction(tx_id: int, username: str, t_type: str, category: str, amount: float, date: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "UPDATE transactions SET type=?, category=?, amount=?, date=? WHERE id=? AND username=?",
        (t_type, category, float(amount), date, tx_id, username),
    )
    changed = c.rowcount
    conn.commit()
    conn.close()
    return changed > 0

def delete_transaction(tx_id: int, username: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM transactions WHERE id = ? AND username = ?", (tx_id, username))
    changed = c.rowcount
    conn.commit()
    conn.close()
    return changed > 0
# ... (existing code in database.py) ...

# --- User Goals ---
def init_db():
    # ... (keep your existing init_db code) ...
    
    # ADD THIS NEW TABLE CREATION inside your existing init_db function:
    # (Or if you prefer, add it as a separate function, but putting it here ensures it runs on startup)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS user_goals (
            username TEXT PRIMARY KEY,
            goal_amount REAL NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

def get_user_goal(username: str) -> Optional[float]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT goal_amount FROM user_goals WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0]
    return None # Returns None if no goal is set yet

def set_user_goal(username: str, amount: float):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # INSERT OR REPLACE updates the row if username exists, or creates it if it doesn't
    c.execute("INSERT OR REPLACE INTO user_goals (username, goal_amount) VALUES (?, ?)", (username, amount))
    conn.commit()
    conn.close()