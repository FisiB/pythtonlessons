import os
import re
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

load_dotenv()

# Security: Require .env file
JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise ValueError("JWT_SECRET is missing in .env file.")

JWT_ALGO = os.getenv("JWT_ALGO", "HS256")
ACCESS_TOKEN_EXPIRES_MINUTES = 60 * 24 * 7

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

# --- Helpers ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp": expire, "iat": now})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGO)
    return encoded_jwt

def verify_token(auth_header: Optional[str] = Header(None)) -> str:
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

@app.on_event("startup")
def startup():
    database.init_db()

# --- Auth ---
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

# --- Transactions ---
@app.post("/transactions", response_model=TransactionOut)
def create_transaction(tx: TransactionIn, username: str = Depends(verify_token)):
    tx_id = database.add_transaction(username, tx.type, tx.category or "", tx.amount, tx.date)
    out = {
        "id": tx_id, "username": username, "type": tx.type, 
        "category": tx.category or "", "amount": tx.amount, 
        "date": tx.date or datetime.utcnow().strftime("%Y-%m-%d")
    }
    return out

@app.get("/transactions/me", response_model=List[TransactionOut])
def list_my_transactions(username: str = Depends(verify_token)):
    df = database.get_transactions(username)
    if df is None or df.empty:
        return []
    rows = df.to_dict(orient="records")
    out = []
    for r in rows:
        out.append({
            "id": int(r["id"]), "username": r["username"], "type": r["type"], 
            "category": r["category"], "amount": float(r["amount"]), "date": r["date"]
        })
    return out

@app.delete("/transactions/{tx_id}")
def remove_transaction(tx_id: int, username: str = Depends(verify_token)):
    ok = database.delete_transaction(tx_id, username)
    if not ok:
        raise HTTPException(status_code=404, detail="Transaction not found or not owned by user")
    return {"message": "deleted"}

# --- New Features ---

@app.get("/scrape-currency")
def scrape_currency(frm: str = "EUR", to: str = "USD"):
    """
    Scrapes exchange rate from Yahoo Finance.
    Allowed: finance.yahoo.com
    """
    allowed_domains = ["finance.yahoo.com"]
    target_url = f"https://finance.yahoo.com/quote/{frm}{to}=X"
    
    # Basic SSRF Protection
    if not any(d in target_url for d in allowed_domains):
        raise HTTPException(status_code=400, detail="Domain not allowed")

    try:
        # Headers to mimic a real browser slightly better
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        res = requests.get(target_url, headers=headers, timeout=10)
        res.raise_for_status()
        
        soup = BeautifulSoup(res.text, "html.parser")
        # Yahoo Finance usually puts the rate in a <fin-streamer> tag or a specific span
        # This selector often works for the main rate
        rate_tag = soup.find("fin-streamer", {"data-field": "regularMarketPrice"})
        
        if rate_tag:
            return {"source": "Yahoo Finance", "from": frm, "to": to, "rate": float(rate_tag.text.replace(",",""))}
        else:
            # Fallback logic if tags change
            return {"source": "Yahoo Finance (Fallback)", "from": frm, "to": to, "rate": 1.0, "note": "Could not parse specific rate tag"}
            
    except Exception as e:
        # Fallback so the app doesn't crash during presentation if scraping fails
        return {"source": "Mock Data", "from": frm, "to": to, "rate": 1.1, "note": "Scraping failed, using mock rate"}

@app.get("/ai-tips")
def get_ai_tips(username: str = Depends(verify_token)):
    """
    Analyzes user data and returns tips.
    """
    df = database.get_transactions(username)
    if df is None or df.empty:
        return {"tips": ["Add some transactions to get personalized advice!"]}
    
    income = df[df["type"] == "income"]["amount"].sum()
    expense = df[df["type"] == "expense"]["amount"].sum()
    
    tips = []
    if income == 0:
        tips.append("⚠️ You have no recorded income yet.")
    
    savings_rate = 0
    if income > 0:
        savings_rate = ((income - expense) / income) * 100
        tips.append(f"📊 Your savings rate is {savings_rate:.1f}%.")
    
    if savings_rate < 10:
        tips.append("🛑 Tip: Try to save at least 20% of your income.")
    elif savings_rate >= 20:
        tips.append("🌟 Great job! You are saving a healthy amount.")
        
    if expense > income:
        tips.append("🚨 Alert: You are spending more than you earn!")
        
    # Find most expensive category
    expenses = df[df["type"] == "expense"]
    if not expenses.empty:
        top_cat = expenses.groupby("category")["amount"].sum().idxmax()
        tips.append(f"💡 Your biggest expense is '{top_cat}'. Check if you can reduce this.")
        
    return {"tips": tips}