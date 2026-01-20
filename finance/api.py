"""
api.py
FastAPI app with:
- /auth/register  (POST) : register user
- /auth/login     (POST) : returns JWT token
- /transactions   (GET/POST/DELETE) : requires Bearer token
- /scrape         (GET) : simple scraper using requests + BeautifulSoup

Run:
  uvicorn api:app --reload --port 8000
"""
import os
from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

import database

# load .env (if present)
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_ALGO = os.getenv("JWT_ALGO", "HS256")
ACCESS_TOKEN_EXPIRES_MINUTES = 60 * 24 * 7  # 7 days

API_ALLOWED_ORIGINS = ["http://localhost:8501", "http://127.0.0.1:8501"]

app = FastAPI(title="Finance Minimal API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=API_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AuthPayload(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TransactionIn(BaseModel):
    type: str
    category: Optional[str] = ""
    amount: float
    date: Optional[str] = None


class TransactionOut(TransactionIn):
    id: int
    username: str


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp": expire, "iat": now})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGO)
    return encoded_jwt


def verify_token(auth_header: Optional[str] = Header(None)) -> str:
    """
    Dependency that extracts username from Authorization header "Bearer <token>".
    Returns username or raises HTTPException.
    """
    if not auth_header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    parts = auth_header.split()
    if parts[0].lower() != "bearer" or len(parts) != 2:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")
    token = parts[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalid or expired")


# Startup: ensure DB exists
@app.on_event("startup")
def startup():
    database.init_db()


# --- Auth routes ---
@app.post("/auth/register", status_code=201)
def register(auth: AuthPayload):
    ok = database.register_user(auth.username, auth.password)
    if not ok:
        raise HTTPException(status_code=400, detail="Username exists or invalid input")
    return {"message": "user created"}


@app.post("/auth/login", response_model=Token)
def login(auth: AuthPayload):
    if not database.authenticate_user(auth.username, auth.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": auth.username})
    return {"access_token": access_token}


# --- Transaction routes ---
@app.post("/transactions", response_model=TransactionOut)
def create_transaction(tx: TransactionIn, username: str = Depends(verify_token)):
    tx_id = database.add_transaction(username, tx.type, tx.category or "", tx.amount, tx.date)
    out = {"id": tx_id, "username": username, "type": tx.type, "category": tx.category or "", "amount": tx.amount, "date": tx.date or datetime.utcnow().strftime("%Y-%m-%d")}
    return out


@app.get("/transactions/me", response_model=List[TransactionOut])
def list_my_transactions(username: str = Depends(verify_token)):
    df = database.get_transactions(username)
    if df is None or df.empty:
        return []
    rows = df.to_dict(orient="records")
    # adapt records to TransactionOut
    out = []
    for r in rows:
        out.append({"id": int(r["id"]), "username": r["username"], "type": r["type"], "category": r["category"], "amount": float(r["amount"]), "date": r["date"]})
    return out


@app.delete("/transactions/{tx_id}")
def remove_transaction(tx_id: int, username: str = Depends(verify_token)):
    ok = database.delete_transaction(tx_id, username)
    if not ok:
        raise HTTPException(status_code=404, detail="Transaction not found or not owned by user")
    return {"message": "deleted"}


# --- Scraping endpoint (simple) ---
@app.get("/scrape")
def scrape(url: str):
    """
    Simple scraping endpoint that returns the page title and first paragraph.
    Use with care. No heavy scraping or automated bursts.
    """
    try:
        res = requests.get(url, timeout=8, headers={"User-Agent": "finance-minimal-bot/0.1"})
        res.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {e}")
    soup = BeautifulSoup(res.text, "html.parser")
    title = soup.title.string.strip() if soup.title else ""
    p = soup.find("p")
    first_p = p.get_text().strip() if p else ""
    return {"title": title, "first_paragraph": first_p}