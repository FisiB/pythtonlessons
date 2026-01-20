"""
web.py
Streamlit frontend that calls the FastAPI backend (api.py).
- Login / Sign Up communicate with /auth endpoints
- Transactions, scraping, stats call API endpoints and render charts
Run:
  1) Start API:   uvicorn api:app --reload --port 8000
  2) Start UI:    streamlit run web.py
"""
import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

load_dotenv()

API_HOST = os.getenv("API_HOST", "http://127.0.0.1:8000")

st.set_page_config(page_title="Finance App (Minimal)", layout="wide")

# session helpers
def set_token(token: str, username: str):
    st.session_state["token"] = token
    st.session_state["username"] = username


def get_token():
    return st.session_state.get("token")


def get_username():
    return st.session_state.get("username")


def clear_session():
    for k in ["token", "username"]:
        if k in st.session_state:
            del st.session_state[k]


def auth_headers():
    token = get_token()
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


# UI: sidebar
st.sidebar.title("Menu")
menu = st.sidebar.radio("", ["Login / Sign Up", "Dashboard", "Currency", "Transactions", "Statistics", "Scrape site", "Logout"])

# Login / Sign Up form
if menu == "Login / Sign Up":
    st.title("🔐 Authentication")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Login")
        lu = st.text_input("Username (login)", key="lu")
        lp = st.text_input("Password", type="password", key="lp")
        if st.button("Login"):
            try:
                r = requests.post(f"{API_HOST}/auth/login", json={"username": lu, "password": lp}, timeout=8)
                if r.status_code == 200:
                    token = r.json()["access_token"]
                    set_token(token, lu)
                    st.success("Logged in")
                else:
                    st.error(r.json().get("detail", "Login failed"))
            except Exception as e:
                st.error(f"Error contacting API: {e}")
    with col2:
        st.subheader("Sign Up")
        su = st.text_input("Choose username", key="su")
        sp = st.text_input("Choose password", type="password", key="sp")
        if st.button("Sign Up"):
            try:
                r = requests.post(f"{API_HOST}/auth/register", json={"username": su, "password": sp}, timeout=8)
                if r.status_code in (200, 201):
                    st.success("User created — please log in")
                else:
                    st.error(r.json().get("detail", "Sign up failed"))
            except Exception as e:
                st.error(f"Error contacting API: {e}")

# Dashboard
elif menu == "Dashboard":
    st.title("🏠 Dashboard")
    username = get_username()
    if not username:
        st.info("Please log in first.")
    else:
        # fetch transactions
        try:
            r = requests.get(f"{API_HOST}/transactions/me", headers=auth_headers(), timeout=8)
            if r.status_code == 200:
                txs = r.json()
                if not txs:
                    st.info("No transactions yet. Add from Transactions page.")
                else:
                    df = pd.DataFrame(txs)
                    df["amount"] = df["amount"].astype(float)
                    income = df[df["type"] == "income"]["amount"].sum()
                    expense = df[df["type"] == "expense"]["amount"].sum()
                    balance = income - expense
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Balance", f"${balance:,.2f}")
                    c2.metric("Income", f"${income:,.2f}")
                    c3.metric("Expenses", f"${expense:,.2f}")
                    st.subheader("Recent")
                    st.dataframe(df.head(10), use_container_width=True)
            else:
                st.error("Failed to fetch transactions")
        except Exception as e:
            st.error(f"API error: {e}")

# Currency converter (client-side)
elif menu == "Currency":
    st.title("💱 Currency Converter")
    username = get_username()
    if not username:
        st.info("Login to use features.")
    else:
        amt = st.number_input("Amount", min_value=0.0, format="%.2f")
        rate = st.number_input("Rate", min_value=0.0, format="%.6f")
        if st.button("Convert"):
            res = amt * rate
            st.success(f"{amt} at rate {rate} = {res:.2f}")

# Transactions: add & list via API
elif menu == "Transactions":
    st.title("💳 Transactions")
    username = get_username()
    if not username:
        st.info("Please log in first.")
    else:
        with st.form("tx"):
            ttype = st.selectbox("Type", ["income", "expense"])
            category = st.text_input("Category")
            amount = st.number_input("Amount", min_value=0.0, format="%.2f")
            date = st.date_input("Date")
            sub = st.form_submit_button("Add")
        if sub:
            payload = {"type": ttype, "category": category or "", "amount": float(amount), "date": date.strftime("%Y-%m-%d")}
            try:
                r = requests.post(f"{API_HOST}/transactions", json=payload, headers=auth_headers(), timeout=8)
                if r.status_code == 200:
                    st.success("Added")
                else:
                    st.error(r.json().get("detail", "Failed to add"))
            except Exception as e:
                st.error(f"API error: {e}")

        # list
        try:
            r = requests.get(f"{API_HOST}/transactions/me", headers=auth_headers(), timeout=8)
            if r.status_code == 200:
                txs = r.json()
                if not txs:
                    st.info("No transactions.")
                else:
                    df = pd.DataFrame(txs)
                    st.dataframe(df, use_container_width=True)
                    st.write("---")
                    st.write("Delete by id:")
                    ids = df["id"].tolist()
                    sel = st.selectbox("ID", options=[None] + ids)
                    if st.button("Delete selected"):
                        if sel:
                            try:
                                r2 = requests.delete(f"{API_HOST}/transactions/{sel}", headers=auth_headers(), timeout=8)
                                if r2.status_code == 200:
                                    st.success("Deleted")
                                else:
                                    st.error(r2.json().get("detail", "Failed"))
                            except Exception as e:
                                st.error(f"API error: {e}")
                        else:
                            st.info("Select id first")
            else:
                st.error("Failed to fetch transactions")
        except Exception as e:
            st.error(f"API error: {e}")

# Statistics + visualizations
elif menu == "Statistics":
    st.title("📊 Statistics")
    username = get_username()
    if not username:
        st.info("Please login first.")
    else:
        try:
            r = requests.get(f"{API_HOST}/transactions/me", headers=auth_headers(), timeout=8)
            if r.status_code == 200:
                txs = r.json()
                if not txs:
                    st.info("No data.")
                else:
                    df = pd.DataFrame(txs)
                    df["amount"] = df["amount"].astype(float)
                    df["date"] = pd.to_datetime(df["date"])
                    expenses = df[df["type"] == "expense"]
                    if not expenses.empty:
                        monthly = expenses.groupby(pd.Grouper(key="date", freq="M"))["amount"].sum().reset_index()
                        fig = px.bar(monthly, x="date", y="amount", title="Monthly expenses")
                        st.plotly_chart(fig, use_container_width=True)

                        bycat = expenses.groupby("category")["amount"].sum().reset_index()
                        fig2 = px.pie(bycat, names="category", values="amount", title="Expenses by category")
                        st.plotly_chart(fig2, use_container_width=True)
                    else:
                        st.info("No expenses to chart.")
            else:
                st.error("Failed to fetch transactions")
        except Exception as e:
            st.error(f"API error: {e}")

# Scraping small demo
elif menu == "Scrape site":
    st.title("🔎 Scrape a site (demo)")
    url = st.text_input("URL to scrape (example: https://example.com)")
    if st.button("Fetch"):
        if not url:
            st.info("Enter a URL")
        else:
            try:
                r = requests.get(f"{API_HOST}/scrape", params={"url": url}, timeout=10)
                if r.status_code == 200:
                    j = r.json()
                    st.subheader(j.get("title", "No title"))
                    st.write(j.get("first_paragraph", "No paragraph found"))
                else:
                    st.error(r.json().get("detail", "Failed to scrape"))
            except Exception as e:
                st.error(f"Error contacting API: {e}")

# Logout
elif menu == "Logout":
    clear_session()
    st.info("You are logged out.")