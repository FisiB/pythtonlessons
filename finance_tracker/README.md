# Personal Finance Tracker

This folder contains a personal finance tracker example built with Streamlit (frontend), FastAPI (optional API layer), and SQLite for storage.

Quick start (Streamlit):
1. python -m venv .venv
2. .venv/bin/pip install -r requirements.txt
3. cd finance_tracker
4. streamlit run web/app.py

The app will create a local SQLite database at data/transactions.db when it first runs.

Notes:
- Passwords are stored in plain text in this example for simplicity. Do NOT do this in production — hash and salt passwords.
- The FastAPI app is available at api/main.py (run with `uvicorn api.main:app --reload` from inside the finance_tracker folder).
