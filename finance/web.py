import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()

API_HOST = os.getenv("API_HOST", "http://127.0.0.1:8000")

st.set_page_config(page_title="Finance App", layout="wide")

# --- Session Helpers ---
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

# ==========================================
# LOGGED OUT SECTION
# ==========================================
if not get_token():
    st.title("🔐 Finance App Login")
    st.markdown("Welcome to the Finance App. Please log in to manage your wealth.")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.form("login_form"):
            st.subheader("Login")
            lu = st.text_input("Username")
            lp = st.text_input("Password", type="password")
            submitted_login = st.form_submit_button("Login")
            
        if submitted_login:
            try:
                r = requests.post(f"{API_HOST}/auth/login", json={"username": lu, "password": lp}, timeout=8)
                if r.status_code == 200:
                    token = r.json()["access_token"]
                    set_token(token, lu)
                    st.success("Logged in!")
                    st.rerun()
                else:
                    st.error(r.json().get("detail", "Login failed"))
            except Exception as e:
                st.error(f"Error contacting API: {e}")

    with col2:
        with st.form("signup_form"):
            st.subheader("Sign Up")
            su = st.text_input("Choose username", key="su")
            sp = st.text_input("Choose password", type="password", key="sp")
            submitted_signup = st.form_submit_button("Sign Up")
            
        if submitted_signup:
            try:
                r = requests.post(f"{API_HOST}/auth/register", json={"username": su, "password": sp}, timeout=8)
                if r.status_code in (200, 201):
                    st.success("User created — please log in")
                else:
                    st.error(r.json().get("detail", "Sign up failed"))
            except Exception as e:
                st.error(f"Error contacting API: {e}")
    st.stop() 

# ==========================================
# LOGGED IN SECTION
# ==========================================
username = get_username()

st.sidebar.title(f"👋 {username}")
menu = st.sidebar.radio("Navigate", ["Home", "Dashboard", "Currency Converter", "Transactions", "Statistics", "Budget Goals", "Logout"])

# 1. HOME PAGE
if menu == "Home":
    st.title("🏠 Welcome to Your Finance Hub")
    st.markdown("""
    This application helps you track, analyze, and optimize your personal finances.
    
    ### What you can do:
    - **Dashboard:** View your overall balance, income, and expenses at a glance.
    - **Currency Converter:** Use live web scraping to check exchange rates (e.g., EUR to USD).
    - **Transactions:** Add income and expenses, and see immediate visual charts of where your money goes.
    - **Statistics:** Get deep insights and AI-driven tips on how to maximize your savings.
    - **Budget Goals:** (New!) Set a monthly savings target and track your progress.
    """)

# 2. DASHBOARD
elif menu == "Dashboard":
    st.title("📊 Dashboard")
    try:
        r = requests.get(f"{API_HOST}/transactions/me", headers=auth_headers(), timeout=8)
        if r.status_code == 200:
            txs = r.json()
            if not txs:
                st.info("No transactions yet. Go to 'Transactions' to add some.")
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
                st.subheader("Recent Activity")
                st.dataframe(df.head(10), use_container_width=True)
        else:
            st.error("Failed to fetch transactions")
    except Exception as e:
        st.error(f"API error: {e}")

# 3. CURRENCY CONVERTER (SCRAPING)
elif menu == "Currency Converter":
    st.title("💱 Live Currency Scraper")
    st.write("Convert currencies using live data scraped from Yahoo Finance.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        frm = st.text_input("From (e.g., EUR)", value="EUR").upper()
    with col2:
        to = st.text_input("To (e.g., USD)", value="USD").upper()
    with col3:
        amt = st.number_input("Amount", min_value=0.0, value=1.0)
    
    if st.button("Get Live Rate"):
        try:
            r = requests.get(f"{API_HOST}/scrape-currency", params={"frm": frm, "to": to}, timeout=10)
            if r.status_code == 200:
                data = r.json()
                rate = data.get("rate")
                source = data.get("source")
                st.success(f"Live Rate ({source}): 1 {frm} = {rate} {to}")
                result = amt * float(rate)
                st.metric("Converted Value", f"{result:.2f} {to}")
            else:
                st.error("Could not fetch rate.")
        except Exception as e:
            st.error(f"Error: {e}")

# 4. TRANSACTIONS (ADD + CHARTS)
elif menu == "Transactions":
    st.title("💳 Income & Expenses")
    
    # Add Transaction Form
    with st.expander("Add New Transaction", expanded=True):
        with st.form("tx_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                ttype = st.selectbox("Type", ["income", "expense"])
                amount = st.number_input("Amount", min_value=0.0, format="%.2f")
            with col_b:
                category = st.text_input("Category (e.g., Food, Salary)")
                date = st.date_input("Date")
            
            if st.form_submit_button("Add Transaction"):
                # FIX: Check if logged in before sending request
                headers = auth_headers()
                if not headers:
                    st.error("You are not logged in. Please refresh the page or log in again.")
                else:
                    payload = {"type": ttype, "category": category or "Misc", "amount": float(amount), "date": date.strftime("%Y-%m-%d")}
                    try:
                        r = requests.post(f"{API_HOST}/transactions", json=payload, headers=headers, timeout=8)
                        if r.status_code == 200:
                            st.success("Transaction added!")
                            st.rerun()
                        else:
                            st.error(r.json().get("detail", "Failed"))
                    except Exception as e:
                        st.error(f"API error: {e}")

    st.markdown("---")
    
    # List Transactions and Show Charts
    try:
        r = requests.get(f"{API_HOST}/transactions/me", headers=auth_headers(), timeout=8)
        if r.status_code == 200:
            txs = r.json()
            if not txs:
                st.info("No transactions to display.")
            else:
                df = pd.DataFrame(txs)
                
                # Show Charts immediately after data
                st.subheader("📊 Visual Overview")
                c1, c2 = st.columns(2)
                
                with c1:
                    st.write("Income vs Expense")
                    inc_exp = df.groupby("type")["amount"].sum().reset_index()
                    fig_pie = px.pie(inc_exp, values="amount", names="type", hole=0.4)
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                with c2:
                    st.write("Spending by Category")
                    expenses = df[df["type"] == "expense"]
                    if not expenses.empty:
                        cat_data = expenses.groupby("category")["amount"].sum().reset_index()
                        fig_bar = px.bar(cat_data, x="category", y="amount", color="category")
                        st.plotly_chart(fig_bar, use_container_width=True)

                # Delete Section
                st.subheader("Manage Transactions")
                st.dataframe(df, use_container_width=True)
                with st.form("delete_form"):
                    ids = df["id"].tolist()
                    sel = st.selectbox("Select ID to delete", options=[None] + ids)
                    if st.form_submit_button("Delete"):
                        if sel:
                            requests.delete(f"{API_HOST}/transactions/{sel}", headers=auth_headers(), timeout=8)
                            st.rerun()
    except Exception as e:
        st.error(f"API error: {e}")

# 5. STATISTICS (ANALYSIS + TIPS)
elif menu == "Statistics":
    st.title("📈 Advanced Statistics & Tips")
    
    # Fetch AI Tips
    st.subheader("💡 AI Financial Tips")
    try:
        r = requests.get(f"{API_HOST}/ai-tips", headers=auth_headers(), timeout=8)
        if r.status_code == 200:
            tips_data = r.json()
            for tip in tips_data.get("tips", []):
                st.info(tip)
    except Exception as e:
        st.error("Could not load tips.")

    st.markdown("---")
    st.subheader("📉 Profit Maximization Analysis")
    try:
        r = requests.get(f"{API_HOST}/transactions/me", headers=auth_headers(), timeout=8)
        if r.status_code == 200:
            txs = r.json()
            if not txs:
                st.info("No data available.")
            else:
                df = pd.DataFrame(txs)
                df["date"] = pd.to_datetime(df["date"])
                df["amount"] = df["amount"].astype(float)
                
                # Monthly Profit Trend
                monthly = df.groupby([pd.Grouper(key="date", freq="M"), "type"])["amount"].sum().unstack(fill_value=0)
                monthly["balance"] = monthly.get("income", 0) - monthly.get("expense", 0)
                
                fig = px.line(monthly, x=monthly.index, y="balance", markers=True, title="Monthly Net Profit Trend")
                st.plotly_chart(fig, use_container_width=True)
                
                st.write("This chart shows your true profitability. If the line goes down, you are losing money that month.")
    except Exception as e:
        st.error(f"API error: {e}")

# 6. BUDGET GOALS (AI Suggestion Feature)
elif menu == "Budget Goals":
    st.title("🎯 Budget Goals")
    st.write("Set a savings goal and track your progress.")
    
    # Initialize goal in session state if not exists
    if "budget_goal" not in st.session_state:
        st.session_state["budget_goal"] = 1000.0
    
    goal = st.number_input("Set your Monthly Savings Goal ($)", value=st.session_state["budget_goal"], min_value=0.0)
    st.session_state["budget_goal"] = goal
    
    # Calculate current savings
    try:
        r = requests.get(f"{API_HOST}/transactions/me", headers=auth_headers(), timeout=8)
        if r.status_code == 200:
            txs = r.json()
            if txs:
                df = pd.DataFrame(txs)
                df["date"] = pd.to_datetime(df["date"])
                df["amount"] = df["amount"].astype(float)
                
                # Calculate savings for current month
                now = pd.Timestamp.now()
                current_month_data = df[(df["date"].dt.month == now.month) & (df["date"].dt.year == now.year)]
                
                income = current_month_data[current_month_data["type"] == "income"]["amount"].sum()
                expense = current_month_data[current_month_data["type"] == "expense"]["amount"].sum()
                current_savings = income - expense
                
                st.metric("Current Month Savings", f"${current_savings:.2f}")
                st.metric("Goal", f"${goal:.2f}")
                
                # Progress Bar
                percent = min(max((current_savings / goal) * 100, 0), 100) if goal > 0 else 0
                st.progress(percent / 100)
                st.write(f"Progress: {percent:.1f}%")
                
                if current_savings >= goal:
                    st.success("🎉 Congratulations! You reached your goal!")
                elif current_savings < 0:
                    st.warning("You are currently in deficit for this month.")
                else:
                    st.info(f"You need ${goal - current_savings:.2f} more to reach your goal.")
    except Exception as e:
        st.error("Could not load data for goals.")

# 7. LOGOUT
elif menu == "Logout":
    clear_session()
    st.info("You have been logged out.")
    st.rerun()