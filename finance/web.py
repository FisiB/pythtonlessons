import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

load_dotenv()

API_HOST = os.getenv("API_HOST", "http://127.0.0.1:8000")

st.set_page_config(page_title="Finance Tracker", layout="wide")

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
    # Explicitly defining the header key
    return {"Authorization": f"Bearer {token}"}

# ==========================================
# LOGGED OUT SECTION
# ==========================================
if not get_token():
    st.title("💰 Finance Tracker Login")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.form("login_form"):
            st.subheader("Login")
            lu = st.text_input("Username")
            lp = st.text_input("Password", type="password")
            submitted_login = st.form_submit_button("Login", use_container_width=True)
            
        if submitted_login:
            try:
                r = requests.post(f"{API_HOST}/auth/login", json={"username": lu, "password": lp}, timeout=8)
                if r.status_code == 200:
                    token = r.json().get("access_token")
                    if token:
                        set_token(token, lu)
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error("Login failed: No token received.")
                else:
                    st.error(r.json().get("detail", "Invalid credentials"))
            except Exception as e:
                st.error(f"Connection Error: {e}")

    with col2:
        with st.form("signup_form"):
            st.subheader("Sign Up")
            su = st.text_input("Choose username", key="su")
            sp = st.text_input("Choose password", type="password", key="sp")
            submitted_signup = st.form_submit_button("Sign Up", use_container_width=True)
            
        if submitted_signup:
            try:
                r = requests.post(f"{API_HOST}/auth/register", json={"username": su, "password": sp}, timeout=8)
                if r.status_code in (200, 201):
                    st.success("Account created! Please log in.")
                else:
                    st.error(r.json().get("detail", "Sign up failed"))
            except Exception as e:
                st.error(f"Connection Error: {e}")
    st.stop() 

# ==========================================
# LOGGED IN SECTION
# ==========================================
username = get_username()

st.sidebar.title(f"👋 {username}")

# Debug Toggle for Auth Issues
debug_mode = st.sidebar.checkbox("Debug Mode (Show Token)", value=False)
if debug_mode:
    st.sidebar.write("Current Token:", get_token())

menu = st.sidebar.radio("Navigate", ["Home", "Transactions", "Budget Goals", "Currency Converter", "Logout"])

# Helper function to fetch transactions (used in multiple pages)
@st.cache_data(ttl=60) # Cache for 60 seconds
def fetch_transactions():
    headers = auth_headers()
    if not headers:
        return None
    try:
        r = requests.get(f"{API_HOST}/transactions/me", headers=headers, timeout=8)
        if r.status_code == 200:
            return r.json()
        else:
            st.error(f"Error fetching data: {r.status_code}")
            return None
    except Exception as e:
        st.error(f"API Connection error: {e}")
        return None

# 1. HOME PAGE
if menu == "Home":
    st.title("🏠 Welcome Back!")
    st.markdown(f"Hello **{username}**, here is your financial overview.")
    
    txs = fetch_transactions()
    
    if txs:
        df = pd.DataFrame(txs)
        df["amount"] = df["amount"].astype(float)
        
        total_income = df[df["type"] == "income"]["amount"].sum()
        total_expense = df[df["type"] == "expense"]["amount"].sum()
        balance = total_income - total_expense
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Balance", f"${balance:,.2f}", delta=f"${balance:,.2f}")
        c2.metric("Total Income", f"${total_income:,.2f}", delta_color="normal")
        c3.metric("Total Expenses", f"${total_expense:,.2f}", delta_color="inverse")
        
        st.info("👉 Use the sidebar to navigate to **Transactions** to manage your money or **Budget Goals** to track targets.")
    else:
        st.warning("No transaction data found.")

# 2. TRANSACTIONS (IMPROVED WITH TABS & CHARTS)
elif menu == "Transactions":
    st.title("💳 Manage Transactions")
    
    txs = fetch_transactions()
    df = pd.DataFrame(txs) if txs else pd.DataFrame()
    
    # Use Tabs for better UI
    tab1, tab2, tab3 = st.tabs(["➕ Add New", "📊 Charts", "📜 History"])

    with tab1:
        with st.form("tx_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                ttype = st.selectbox("Type", ["income", "expense"])
                amount = st.number_input("Amount", min_value=0.0, format="%.2f")
            with col_b:
                category = st.text_input("Category", placeholder="e.g. Food, Salary")
                date = st.date_input("Date")
            
            submitted = st.form_submit_button("Add Transaction", use_container_width=True, type="primary")
            
            if submitted:
                headers = auth_headers()
                if debug_mode:
                    st.json({"headers": headers, "payload": {
                        "type": ttype, "category": category or "Misc", 
                        "amount": float(amount), "date": date.strftime("%Y-%m-%d")
                    }})
                
                try:
                    r = requests.post(
                        f"{API_HOST}/transactions", 
                        json={
                            "type": ttype, 
                            "category": category or "Misc", 
                            "amount": float(amount), 
                            "date": date.strftime("%Y-%m-%d")
                        }, 
                        headers=headers, 
                        timeout=8
                    )
                    
                    if r.status_code == 200:
                        st.success("Transaction added successfully!")
                        st.cache_data.clear() # Clear cache so new data appears immediately
                        st.rerun()
                    else:
                        err = r.json().get("detail", r.text)
                        st.error(f"Failed to add: {err}")
                        if "Authorization" in err:
                            st.error("⚠️ Backend Error: The API endpoint is rejecting the header. Check your Backend code.")
                except Exception as e:
                    st.error(f"API Error: {e}")

    with tab2:
        if not df.empty:
            st.subheader("Financial Breakdown")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Income vs Expense**")
                inc_exp = df.groupby("type")["amount"].sum().reset_index()
                fig_pie = px.pie(inc_exp, values="amount", names="type", hole=0.5, 
                                 color_discrete_map={"income": "#00cc96", "expense": "#ef553b"})
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                st.write("**Expenses by Category**")
                expenses = df[df["type"] == "expense"]
                if not expenses.empty:
                    cat_data = expenses.groupby("category")["amount"].sum().reset_index().sort_values("amount", ascending=False)
                    fig_bar = px.bar(cat_data, x="category", y="amount", color="amount", 
                                     color_continuous_scale="Reds")
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("No expenses recorded yet.")
        else:
            st.info("Add transactions to see charts here.")

    with tab3:
        if not df.empty:
            st.dataframe(df.sort_values(by="date", ascending=False), use_container_width=True)
        else:
            st.info("No transactions found.")

# 3. BUDGET GOALS (CONNECTED TO TRANSACTIONS)
elif menu == "Budget Goals":
    st.title("🎯 Budget Goals & Progress")
    
    # Session State for Goal
    if "savings_goal" not in st.session_state:
        st.session_state["savings_goal"] = 1000.0

    # Input Goal
    with st.expander("Set your Savings Goal", expanded=True):
        new_goal = st.number_input("Monthly Savings Target ($)", min_value=0.0, value=st.session_state["savings_goal"])
        if st.button("Update Goal"):
            st.session_state["savings_goal"] = new_goal
            st.success("Goal updated!")
            st.rerun()

    # Fetch Data
    txs = fetch_transactions()
    goal = st.session_state["savings_goal"]

    if txs:
        df = pd.DataFrame(txs)
        df["date"] = pd.to_datetime(df["date"])
        df["amount"] = df["amount"].astype(float)
        
        # Filter for Current Month
        now = pd.Timestamp.now()
        current_month_data = df[(df["date"].dt.month == now.month) & (df["date"].dt.year == now.year)]
        
        # Fallback: If current month is empty, use all data for demonstration
        if current_month_data.empty:
            st.warning("No transactions for **this month** yet. Showing all-time progress.")
            data_source = df
            period_label = "(All Time)"
        else:
            data_source = current_month_data
            period_label = "(This Month)"

        # Calculations
        income = data_source[data_source["type"] == "income"]["amount"].sum()
        expenses = data_source[data_source["type"] == "expense"]["amount"].sum()
        current_savings = income - expenses
        
        # Metrics Row
        m1, m2, m3 = st.columns(3)
        m1.metric("Income", f"${income:,.2f}")
        m2.metric("Expenses", f"${expenses:,.2f}")
        m3.metric("Net Savings", f"${current_savings:,.2f}", delta=f"${current_savings:,.2f}")

        # Progress Logic
        if goal > 0:
            percentage = (current_savings / goal) * 100
        else:
            percentage = 0

        # Visualization: Gauge Chart
        st.subheader(f"Progress to Goal: ${goal:,.2f} {period_label}")
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = current_savings,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"Saved (${current_savings:,.2f})"},
            delta = {'reference': goal},
            gauge = {
                'axis': {'range': [None, goal * 1.2]}, # Axis goes slightly past goal
                'bar': {'color': "#00cc96"},
                'steps': [
                    {'range': [0, goal], 'color': "lightgray"},
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': goal # The goal line
                }
            }
        ))
        
        st.plotly_chart(fig, use_container_width=True)

        # Text Feedback
        if current_savings >= goal:
            st.success("🎉 Amazing! You have reached your savings goal!")
        elif current_savings < 0:
            st.error("⚠️ You are in a deficit. Review your expenses.")
        else:
            amount_left = goal - current_savings
            st.info(f"💡 You need to save **${amount_left:,.2f}** more to reach your goal.")

    else:
        st.info("No data available. Add transactions to track your budget.")

# 4. CURRENCY CONVERTER
elif menu == "Currency Converter":
    st.title("💱 Currency Converter")
    col1, col2, col3 = st.columns(3)
    with col1:
        frm = st.text_input("From", value="USD").upper()
    with col2:
        to = st.text_input("To", value="EUR").upper()
    with col3:
        amt = st.number_input("Amount", min_value=0.0, value=100.0)
    
    if st.button("Convert"):
        try:
            r = requests.get(f"{API_HOST}/scrape-currency", params={"frm": frm, "to": to}, timeout=10)
            if r.status_code == 200:
                data = r.json()
                rate = float(data.get("rate"))
                res = amt * rate
                st.success(f"Rate: 1 {frm} = {rate} {to}")
                st.metric("Result", f"{res:,.2f} {to}")
            else:
                st.error("Failed to fetch rate.")
        except Exception as e:
            st.error(e)

# 5. LOGOUT
elif menu == "Logout":
    clear_session()
    st.success("Logged out successfully.")
    st.rerun()