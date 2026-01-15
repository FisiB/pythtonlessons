import sqlite3
import pandas as pd
import os
from typing import Optional, List, Dict

# Database path (relative to the finance_tracker folder)
DB_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
DB_PATH = os.path.normpath(os.path.join(DB_DIR, 'transactions.db'))

def _ensure_data_dir():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_db() -> None:
    """Create the database and required tables if they do not exist."""
    _ensure_data_dir()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY,
                  username TEXT,
                  type TEXT,
                  category TEXT,
                  amount REAL,
                  date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY,
                  username TEXT UNIQUE,
                  password TEXT)''')
    conn.commit()
    conn.close()

# --- Users ---
def register_user(username: str, password: str) -> bool:
    """Register a new user. Returns True on success, False if username exists."""
    _ensure_data_dir()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username: str, password: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# --- Transactions ---
def add_transaction(username: str, t_type: str, category: str, amount: float, date: Optional[str]) -> None:
    _ensure_data_dir()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO transactions (username, type, category, amount, date) VALUES (?,?,?,?,?)",
              (username, t_type, category, float(amount), date))
    conn.commit()
    conn.close()

def get_transactions(username: str):
    _ensure_data_dir()
    conn = sqlite3.connect(DB_PATH)
    # Use parameterized query to avoid SQL injection
    df = pd.read_sql_query("SELECT * FROM transactions WHERE username=? ORDER BY date DESC", conn, params=(username,))
    conn.close()
    return df

# --- Utilities ---
def convert_currency(amount: float, rate: float) -> float:
    return float(amount) * float(rate)
