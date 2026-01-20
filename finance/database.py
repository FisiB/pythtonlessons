"""
database.py
Simple SQLite helpers: initialize DB, register/login with bcrypt (passlib),
transaction CRUD, and a small currency conversion helper.
"""
import os
import sqlite3
from typing import Optional, List, Dict
from datetime import datetime
from passlib.context import CryptContext
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
DB_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.environ.get("DATABASE_PATH", os.path.join(DB_DIR, "finance.db"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


# --- Users ---
def register_user(username: str, password: str) -> bool:
    """Register a user. Returns True if created, False on duplicate/invalid input."""
    if not username or not password:
        return False
    _ensure_dir()
    hashed = pwd_context.hash(password)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_password_hash(username: str) -> Optional[str]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None


def authenticate_user(username: str, password: str) -> bool:
    stored = get_password_hash(username)
    if not stored:
        return False
    try:
        return pwd_context.verify(password, stored)
    except Exception:
        return False


# --- Transactions ---
def add_transaction(username: str, t_type: str, category: str, amount: float, date: Optional[str] = None) -> int:
    """Add transaction and return inserted id."""
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


def delete_transaction(tx_id: int, username: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM transactions WHERE id = ? AND username = ?", (tx_id, username))
    changed = c.rowcount
    conn.commit()
    conn.close()
    return changed > 0


def convert_currency(amount: float, rate: float) -> float:
    return float(amount) * float(rate)